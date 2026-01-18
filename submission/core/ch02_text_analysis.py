
import os
import re
import sys

# Add nepalikit to path
nepalikit_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'nepalikit-main')
if os.path.exists(nepalikit_path) and nepalikit_path not in sys.path:
    sys.path.insert(0, nepalikit_path)

# Import nepalikit components
try:
    from nepalikit.tokenization.tokenizer import Tokenizer
    from nepalikit.preprocessing.TextProcessor import TextProcessor as NepaliTextProcessor
    NEPALIKIT_AVAILABLE = True
except ImportError:
    NEPALIKIT_AVAILABLE = False
    print("Warning: nepalikit not available, using fallback tokenization")


class TextAnalysis:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.stopwords = self._load_stopwords()
        self.stem_dict = self._load_stem_dict()
        
        # Initialize nepalikit tokenizer if available
        if NEPALIKIT_AVAILABLE:
            self.tokenizer = Tokenizer()
            self.text_processor = NepaliTextProcessor(stopwords=list(self.stopwords))
        else:
            self.tokenizer = None
            self.text_processor = None

    def _load_stopwords(self):
        stopwords = set()
        stopwords_path = os.path.join(self.data_dir, 'stopwords.txt')
        if os.path.exists(stopwords_path):
            with open(stopwords_path, 'r', encoding='utf-8') as f:
                stopwords = set(f.read().splitlines())
        return stopwords

    def _load_stem_dict(self):
        # Basic rule-based stems or dictionary for demo
        # In a real app this would be more robust
        return {
            'गर्ने': 'गर',
            'भने': 'भन',
            'गरे': 'गर',
            'गर्न': 'गर',
            'गरेको': 'गर',
            'गर्दै': 'गर',
            'राम्रा': 'राम्रो',
            'राम्री': 'राम्रो',
            'का': 'को',
            'की': 'को',
            'मा': '',
            'हरु': '',
            'हरू': '',
            'लाई': '',
            'ले': '',
            'बाट': '',
        }
    
    def _tokenize_nepalikit(self, text):
        """
        Tokenize using nepalikit's advanced tokenizer.
        Handles Nepali-specific punctuation like '।' and Devanagari script properly.
        """
        # Use nepalikit's word tokenizer with Nepali punctuation support
        tokens = self.tokenizer.word_tokenize(text)
        # Filter out empty tokens
        tokens = [t for t in tokens if t.strip()]
        return tokens
    
    def _tokenize_fallback(self, text):
        """
        Fallback tokenization method if nepalikit is not available.
        Basic unicode-aware tokenization for Nepali.
        """
        # Remove Nepali-specific punctuation
        text = text.replace('।', ' ')
        # Keep Devanagari characters and common punctuation
        clean_text = re.sub(r'[^\u0900-\u097F\s]', '', text)
        # Split and filter
        tokens = clean_text.split()
        return [t for t in tokens if t.strip()]
        
    def analyze_text(self, text):
        results = {}
        
        # Step 1: Raw
        results['raw'] = text
        
        # Step 2: Tokenization (Using nepalikit for better Nepali support)
        if NEPALIKIT_AVAILABLE and self.tokenizer:
            tokens = self._tokenize_nepalikit(text)
            results['tokenization_method'] = 'nepalikit'
        else:
            tokens = self._tokenize_fallback(text)
            results['tokenization_method'] = 'fallback'
            
        results['tokens'] = tokens
        
        # Step 3: Normalization (Stopword Removal)
        filtered = [t for t in tokens if t.lower() not in self.stopwords]
        results['filtered'] = filtered
        results['removed_stopwords'] = list(set(tokens) - set(filtered))
        
        # Step 4: Stemming (Enhanced with more rules)
        stemmed = []
        for token in filtered:
            # Check dictionary first
            if token in self.stem_dict:
                stem = self.stem_dict[token]
                if stem:  # Only add non-empty stems
                    stemmed.append(stem)
            # Enhanced suffix stripping rules for Nepali
            elif len(token) > 3:  # Only stem words longer than 3 chars
                stemmed_word = token
                # Try multiple suffix removal rules
                for suffix in ['हरू', 'हरु', 'लाई', 'बाट', 'मा', 'को', 'का', 'की', 'ले']:
                    if stemmed_word.endswith(suffix):
                        stemmed_word = stemmed_word[:-len(suffix)]
                        break
                if stemmed_word:  # Add if not empty
                    stemmed.append(stemmed_word)
            else:
                stemmed.append(token)
                
        results['stemmed'] = [s for s in stemmed if s]  # Remove any empty strings
        
        return results
    
    def preprocess_for_indexing(self, text):
        """
        Quick preprocessing pipeline for indexing purposes.
        Returns clean tokens ready for inverted index.
        """
        if NEPALIKIT_AVAILABLE and self.tokenizer:
            tokens = self._tokenize_nepalikit(text)
        else:
            tokens = self._tokenize_fallback(text)
        
        # Remove stopwords
        tokens = [t for t in tokens if t.lower() not in self.stopwords]
        
        # Apply stemming
        stemmed_tokens = []
        for token in tokens:
            if token in self.stem_dict:
                stem = self.stem_dict[token]
                if stem:
                    stemmed_tokens.append(stem)
            else:
                stemmed_tokens.append(token)
        
        return [t.lower() for t in stemmed_tokens if t]


# Backward compatibility for imports
if __name__ == "__main__":
    # Test the improved tokenizer
    analyzer = TextAnalysis('../data')
    
    # Test with Nepali text
    test_text = "नेपालको राजधानी काठमाडौं हो। यो धेरै राम्रो शहर हो।"
    print(f"Test text: {test_text}")
    print(f"Tokenization engine: {'nepalikit' if NEPALIKIT_AVAILABLE else 'fallback'}")
    print()
    
    results = analyzer.analyze_text(test_text)
    
    print(f"Tokens ({len(results['tokens'])}): {results['tokens']}")
    print(f"After stopword removal ({len(results['filtered'])}): {results['filtered']}")
    print(f"Removed stopwords: {results['removed_stopwords']}")
    print(f"After stemming ({len(results['stemmed'])}): {results['stemmed']}")
