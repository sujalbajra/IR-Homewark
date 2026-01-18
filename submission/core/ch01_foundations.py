
import os
import math
import sys
from collections import Counter

# Import improved tokenization from ch02
try:
    from .ch02_text_analysis import TextAnalysis
    IMPROVED_TOKENIZATION = True
except (ImportError, ValueError):
    # Fallback if running as standalone
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from ch02_text_analysis import TextAnalysis
        IMPROVED_TOKENIZATION = True
    except ImportError:
        IMPROVED_TOKENIZATION = False


class Foundations:
    def __init__(self, doc_dir):
        self.doc_dir = doc_dir
        self.docs = self._load_documents()
        
        # Initialize improved tokenizer if available
        if IMPROVED_TOKENIZATION:
            # Get data directory (parent of documents directory)
            data_dir = os.path.dirname(doc_dir) if os.path.isdir(doc_dir) else 'data'
            try:
                self.text_analyzer = TextAnalysis(data_dir)
            except:
                self.text_analyzer = None
        else:
            self.text_analyzer = None
            
        self.inverted_index = self._build_index()

    def _load_documents(self):
        docs = {}
        if os.path.exists(self.doc_dir):
            for filename in os.listdir(self.doc_dir):
                if filename.endswith('.txt'):
                    with open(os.path.join(self.doc_dir, filename), 'r', encoding='utf-8') as f:
                        docs[filename] = f.read()
        return docs

    def _tokenize(self, text):
        """
        Tokenize text using improved Nepali tokenization if available.
        Falls back to basic tokenization if not.
        """
        if self.text_analyzer:
            # Use improved tokenization with nepalikit
            tokens = self.text_analyzer.preprocess_for_indexing(text)
        else:
            # Basic fallback tokenization
            # Remove common punctuation and handle Devanagari
            text = text.replace('।', ' ').replace(',', ' ').replace('.', ' ')
            tokens = [t.lower() for t in text.split() if t.strip()]
        
        return tokens


    def _build_index(self):
        index = {}
        for doc_id, text in self.docs.items():
            tokens = set(self._tokenize(text)) # Set for boolean presence
            for token in tokens:
                if token not in index:
                    index[token] = set()
                index[token].add(doc_id)
        return index

    def boolean_search(self, query, operation='AND'):
        """
        Executes a simple boolean query between two terms.
        Extended to support list of terms for simple demo.
        """
        terms = self._tokenize(query)
        if not terms:
            return set()
            
        result_set = None
        
        for term in terms:
            term_docs = self.inverted_index.get(term, set())
            
            if result_set is None:
                result_set = term_docs.copy()
            else:
                if operation == 'AND':
                    result_set = result_set.intersection(term_docs)
                elif operation == 'OR':
                    result_set = result_set.union(term_docs)
                elif operation == 'NOT':
                    # NOT is generally binary (A NOT B), handling simplistic unary NOT here for demo
                    result_set = result_set.difference(term_docs)
                    
        return list(result_set) if result_set else []

    def compute_cosine_similarity(self, query):
        """
        Computes cosine similarity between query and all documents.
        Returns sorted list of (doc_id, score).
        """
        query_tokens = Counter(self._tokenize(query))
        scores = {}
        
        for doc_id, text in self.docs.items():
            doc_tokens = Counter(self._tokenize(text))
            
            # Dot Product
            dot_product = 0
            all_terms = set(query_tokens.keys()).union(set(doc_tokens.keys()))
            
            for term in all_terms:
                dot_product += query_tokens.get(term, 0) * doc_tokens.get(term, 0)
                
            # Magnitude
            query_mag = math.sqrt(sum(cnt**2 for cnt in query_tokens.values()))
            doc_mag = math.sqrt(sum(cnt**2 for cnt in doc_tokens.values()))
            
            if query_mag * doc_mag == 0:
                scores[doc_id] = 0
            else:
                scores[doc_id] = dot_product / (query_mag * doc_mag)
                
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
