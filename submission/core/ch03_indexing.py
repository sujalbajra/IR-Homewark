
import os
import sys
import pickle
import collections
from .ch02_text_analysis import TextAnalysis

class Indexing:
    def __init__(self, data_dir, doc_dir):
        self.doc_dir = doc_dir
        self.analyzer = TextAnalysis(data_dir)
        self.inverted_index = {}
        self.positional_index = {}
        
    def build_indexes(self):
        """Builds both inverted and positional indexes from disk documents"""
        self.inverted_index = collections.defaultdict(list)
        self.positional_index = collections.defaultdict(lambda: collections.defaultdict(list))
        
        doc_count = 0
        total_tokens = 0
        
        if os.path.exists(self.doc_dir):
            for filename in os.listdir(self.doc_dir):
                if filename.endswith('.txt'):
                    doc_count += 1
                    with open(os.path.join(self.doc_dir, filename), 'r', encoding='utf-8') as f:
                        text = f.read()
                        
                    # Use pipeline for terms
                    analysis = self.analyzer.analyze_text(text)
                    terms = analysis['stemmed'] # Use stemmed terms for index
                    
                    total_tokens += len(terms)
                    
                    # Inverted Index Construction
                    term_set = set(terms)
                    for term in term_set:
                        self.inverted_index[term].append(filename)
                        
                    # Positional Index Construction
                    for pos, term in enumerate(terms):
                        self.positional_index[term][filename].append(pos)
                        
        stats = {
            'doc_count': doc_count,
            'vocab_size': len(self.inverted_index),
            'total_tokens': total_tokens,
            'avg_tokens_per_doc': total_tokens / doc_count if doc_count > 0 else 0
        }
        return stats

    def get_posting_list(self, term):
        """Returns posting list for a term (Inverted Index)"""
        # Simple stemming to match index
        stemmed = self.analyzer.analyze_text(term)['stemmed']
        if not stemmed:
            return []
        term = stemmed[0]
        return self.inverted_index.get(term, [])

    def get_positional_postings(self, term):
        """Returns positional postings for a term"""
        stemmed = self.analyzer.analyze_text(term)['stemmed']
        if not stemmed:
            return {}
        term = stemmed[0]
        # Convert defaultdict to dict for cleaner display
        return dict(self.positional_index.get(term, {}))

    def variable_byte_encode(self, number):
        """Demonstrates Variable Byte Encoding for a single number"""
        bytes_list = []
        while True:
            bytes_list.insert(0, number % 128)
            if number < 128:
                break
            number //= 128
        bytes_list[-1] += 128
        
        # Format as binary strings
        return [f"{b:08b}" for b in bytes_list]

    def compress_dict_demo(self):
        """Demonstrates Dictionary Compression (Front Coding)"""
        # Example specific to Nepali
        terms = ["नेपाल", "नेपाली", "नेपालमा", "नेपालको"]
        
        compressed = []
        # Primitive Front Coding
        # nepal, *i, *ma, *ko (conceptually)
        prefix = "नेपाल"
        compressed.append(f"5नेपाल") # length + term
        compressed.append(f"5*ी")    # shared_len + * + unique
        compressed.append(f"5*मा")
        compressed.append(f"5*को")
        
        return {
            'original': terms,
            'compressed_structure': compressed,
            'savings_pct': 25.0  # Mock calculation
        }
