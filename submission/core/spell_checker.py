
import os
import difflib
from pathlib import Path

class SimpleSpellChecker:
    """
    A simple dictionary-based spell checker using the corpus vocabulary.
    Falls back to this since Hunspell dictionaries (ne_NP) were not found.
    """
    def __init__(self, data_dir=None):
        self.words = set()
        if data_dir is None:
            # Default to submission/data
            base = Path(__file__).resolve().parent.parent
            data_dir = base / 'data'
        
        self.data_dir = Path(data_dir)
        self._load_dictionary()

    def _load_dictionary(self):
        # Load words from corpus
        corpus_path = self.data_dir / 'nepali_corpus.txt'
        if corpus_path.exists():
            with open(corpus_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Simple tokenization
                    tokens = line.strip().split()
                    for t in tokens:
                        # Clean punctuation
                        clean_t = "".join(c for c in t if c.isalnum())
                        if clean_t:
                            self.words.add(clean_t)
        
        # Load words from POS dictionary if available
        pos_path = self.data_dir / 'id_pos_dict.json'
        # Or nepali_pos_dict.txt
        # (Skipping JSON loading to check txt for simplicity or just stick to corpus)
        
        print(f"Loaded {len(self.words)} words into spell checker dictionary.")

    def check(self, word):
        """Check if word is in dictionary."""
        return word in self.words

    def suggest(self, word, n=5, cutoff=0.6):
        """Suggest corrections for a word."""
        if self.check(word):
            return [word]
        
        return difflib.get_close_matches(word, self.words, n=n, cutoff=cutoff)

if __name__ == "__main__":
    checker = SimpleSpellChecker()
    test_words = ["नेपाल", "नपल", "सरकार", "सरकर"]
    for w in test_words:
        print(f"Word: {w}, Correct: {checker.check(w)}, Suggestions: {checker.suggest(w)}")
