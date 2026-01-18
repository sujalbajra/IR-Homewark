
import os
import math
from collections import Counter
from flask import current_app
from .ch02_text_analysis import TextAnalysis

from .pos_tagger import POSTagger
from .nepali_wordnet import IndoWordNet, Synset
from .spell_checker import SimpleSpellChecker

class WordAnalyzer:
    def __init__(self, data_dir, doc_dir):
        self.analyzer = TextAnalysis(data_dir)
        self.doc_dir = doc_dir
        self.documents = self._load_documents()
        self.ner_vocabs = self._load_ner_vocabs()
        self.pos_tagger = POSTagger(data_dir)
        
        # Initialize WordNet (lazy load might be better but it's small)
        self.iwn = IndoWordNet()
        
        # Initialize Spell Checker
        self.spell_checker = SimpleSpellChecker(data_dir=data_dir)
        
        self.df = Counter()
        self.N = len(self.documents)
        self._compute_stats()
        
    def _load_documents(self):
        docs = {}
        if os.path.exists(self.doc_dir):
            for filename in os.listdir(self.doc_dir):
                if filename.endswith('.txt'):
                    with open(os.path.join(self.doc_dir, filename), 'r', encoding='utf-8') as f:
                        docs[filename] = f.read()
        return docs

    def _load_ner_vocabs(self):
        """Load NER vocabulary lists from nerdata directory"""
        vocabs = {}
        ner_dir = None
        
        # Try to get from app config if available (context safe)
        if current_app:
            ner_dir = current_app.config.get('NER_DATA_DIR')
            
        if not ner_dir or not os.path.exists(ner_dir):
             # Fallback logic if config not loaded or path invalid
             # Assume data is in submission/data/nerdata relative to this file
             base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
             ner_dir = os.path.join(base_dir, 'data', 'nerdata')

        if not os.path.exists(ner_dir):
            print(f"Warning: NER directory not found at {ner_dir}")
            return vocabs
            
        # Helper to load file content into set
        def load_vocab(filename):
            path = os.path.join(ner_dir, filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return {line.strip() for line in f if line.strip()}
            return set()

        vocabs['LOC'] = load_vocab('LOC_vocab.txt')
        vocabs['PER'] = load_vocab('PER_vocab.txt')
        vocabs['ORG'] = load_vocab('ORG_vocab.txt')
        vocabs['MISC'] = load_vocab('MISC_vocab.txt')
        vocabs['VIOLENCE'] = load_vocab('VIOLENCE_vocab.txt')
        vocabs['PROFANITY'] = load_vocab('PROFANITY_vocab.txt')
        vocabs['FEEDBACK'] = load_vocab('FEEDBACK_vocab.txt')
        
        return vocabs

    def get_entity_type(self, word):
        """Check if word belongs to any NER vocabulary"""
        for entity_type, vocab in self.ner_vocabs.items():
            if word in vocab:
                return entity_type
        return None

    def _compute_stats(self):
        for text in self.documents.values():
            analysis = self.analyzer.analyze_text(text)
            terms = set(analysis['stemmed'])
            for term in terms:
                self.df[term] += 1

    def analyze_word(self, word, context_doc_id=None):
        """
        Analyze a single word to return linguistic features, WordNet data, and Spell Check.
        """
        analysis = self.analyzer.analyze_text(word)
        original = word
        token = analysis['tokens'][0] if analysis['tokens'] else word
        stem = analysis['stemmed'][0] if analysis['stemmed'] else token
        is_stopword = token.lower() in self.analyzer.stopwords
        entity_type = self.get_entity_type(original) or self.get_entity_type(stem)
        pos_tag = self.pos_tagger.tag_word(original)
        
        # WordNet Lookup
        synsets_data = []
        try:
             synsets = self.iwn.synsets(original)
             # Map simplistic structure
             for s in synsets[:3]: # Limit to top 3
                 synsets_data.append({
                     'name': str(s),
                     'pos': getattr(s, '_pos', 'noun'),
                     'definition': getattr(s, '_gloss', 'No definition available.')
                 })
        except Exception as e:
            print(f"WordNet Lookup Error: {e}")
            
        # Spell Check
        spelling_suggestions = []
        if not self.spell_checker.check(original) and not self.spell_checker.check(stem):
            spelling_suggestions = self.spell_checker.suggest(original)

        # Stats
        doc_freq = self.df.get(stem, 0)
        idf = math.log(self.N / (doc_freq + 1)) if doc_freq > 0 else 0
        
        # TF-IDF in specific document context
        tf_idf = 0.0
        if context_doc_id and context_doc_id in self.documents:
            doc_text = self.documents[context_doc_id]
            doc_analysis = self.analyzer.analyze_text(doc_text)
            doc_terms = doc_analysis['stemmed']
            tf = doc_terms.count(stem)
            tf_idf = tf * idf
            
        return {
            'original': original,
            'stem': stem,
            'is_stopword': is_stopword,
            'entity_type': entity_type,
            'pos_tag': pos_tag,
            'doc_freq': doc_freq,
            'total_docs': self.N,
            'idf': round(idf, 3),
            'tf_idf': round(tf_idf, 3),
            'synsets': synsets_data,
            'spelling_suggestions': spelling_suggestions
        }

    def annotate_document(self, text):
        """
        Annotate document with HTML spans for entities.
        Returns mapped HTML string.
        """
        # We need to preserve whitespace, so we tokenize but keep track of reconstruction
        # Simple approach: Split by space, process words, join back
        # Better approach for exact preservation: regex replacement or careful tokenization
        
        words = text.split(' ') # Basic split to preserve spaces partially
        annotated_words = []
        
        for word in words:
            # Strip punctuation for lookup but keep for display
            clean_word = "".join(c for c in word if c.isalnum())
            
            if not clean_word:
                annotated_words.append(word)
                continue
                
            # Find all matching types
            types = []
            
            # Check original word
            ner_checks = [clean_word, word]
            
            # Check stemmed word
            analysis = self.analyzer.analyze_text(word)
            if analysis['stemmed']:
                ner_checks.append(analysis['stemmed'][0])
                
            for token_check in set(ner_checks):
                for entity_type, vocab in self.ner_vocabs.items():
                    if token_check in vocab:
                        types.append(entity_type)
            
            # Unique types
            types = list(set(types))
            
            if types:
                # Color mapping
                color_map = {
                    'PER': 'primary', 'LOC': 'success', 'ORG': 'info',
                    'MISC': 'warning', 'VIOLENCE': 'danger', 'PROFANITY': 'dark',
                    'FEEDBACK': 'secondary'
                }
                
                main_type = types[0]
                color = color_map.get(main_type, 'secondary')
                type_str = ", ".join(types)
                
                # Create HTML span
                html = f'<span class="entity-highlight badge badge-{color} font-weight-normal" data-toggle="tooltip" title="{type_str}" style="font-size: 0.95em; cursor:help;">{word}</span>'
                annotated_words.append(html)
            else:
                annotated_words.append(word)
                
        return " ".join(annotated_words).replace('\n', '<br>')
