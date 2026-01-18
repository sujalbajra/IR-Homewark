"""
Chapter 15: Enhanced Tokenization
Implements vanilla Python tokenization for Nepali text
Includes sentence, word, character, and n-gram tokenization
"""

import re
import string
from difflib import get_close_matches

class NepaliTokenizer:
    """Enhanced tokenization for Nepali text"""
    
    def __init__(self):
        """Initialize tokenizer with Nepali-specific punctuation"""
        self.nepali_punctuation = ['।', '?', '!', ',', ';', ':', '-', '—', '.']
        
    def sentence_tokenize(self, text):
        """
        Split text into sentences using Nepali sentence markers
        
        Args:
            text: Nepali text string
            
        Returns:
            List of sentences
        """
        # Split on Nepali full stop (।)
        sentences = text.strip().split('।')
        
        # Clean up empty sentences and whitespace
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Also split on ? and ! if present
        final_sentences = []
        for sent in sentences:
            # Further split on question/exclamation marks
            for subsent in re.split(r'[?!]', sent):
                if subsent.strip():
                    final_sentences.append(subsent.strip())
        
        return final_sentences
    
    def word_tokenize(self, text, custom_punctuation=None):
        """
        Split text into words, handling Nepali punctuation
        
        Args:
            text: Nepali text string
            custom_punctuation: Optional list of additional punctuation
            
        Returns:
            List of words
        """
        punctuations = self.nepali_punctuation.copy()
        if custom_punctuation:
            punctuations.extend(custom_punctuation)
        
        # Remove punctuation by replacing with spaces
        for punct in punctuations:
            text = text.replace(punct, ' ')
        
        # Remove English punctuation too
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Split on whitespace and filter empty strings
        words = [word for word in text.split() if word]
        
        return words
    
    def character_tokenize(self, word):
        """
        Split word into individual characters
        
        Args:
            word: Word to tokenize
            
        Returns:
            List of characters
        """
        return list(word)
    
    def generate_ngrams(self, tokens, n=2):
        """
        Generate n-grams from token list
        
        Args:
            tokens: List of tokens (words or characters)
            n: N-gram size
            
        Returns:
            List of n-gram tuples
        """
        if len(tokens) < n:
            return []
        
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            ngrams.append(ngram)
        
        return ngrams
    
    def get_statistics(self, text):
        """
        Get tokenization statistics for text
        
        Args:
            text: Nepali text
            
        Returns:
            Dictionary of statistics
        """
        sentences = self.sentence_tokenize(text)
        all_words = []
        for sent in sentences:
            all_words.extend(self.word_tokenize(sent))
        
        # Count characters (excluding spaces)
        char_count = len(text.replace(' ', ''))
        
        # Generate bigrams and trigrams
        bigrams = self.generate_ngrams(all_words, n=2)
        trigrams = self.generate_ngrams(all_words, n=3)
        
        return {
            'sentences': len(sentences),
            'words': len(all_words),
            'characters': char_count,
            'unique_words': len(set(all_words)),
            'bigrams': len(bigrams),
            'trigrams': len(trigrams),
            'avg_word_length': sum(len(w) for w in all_words) / len(all_words) if all_words else 0,
            'avg_sent_length': len(all_words) / len(sentences) if sentences else 0
        }


class NepaliSpellChecker:
    """Simple spell checker using edit distance"""
    
    def __init__(self, dictionary_path=None):
        """
        Initialize spell checker
        
        Args:
            dictionary_path: Path to dictionary file
        """
        self.dictionary = set()
        if dictionary_path:
            self.load_dictionary(dictionary_path)
    
    def load_dictionary(self, path):
        """Load dictionary from file"""
        with open(path, 'r', encoding='utf-8') as f:
            words = f.read().split('\n')
            self.dictionary = set(word.strip() for word in words if word.strip())
    
    def is_correct(self, word):
        """Check if word is in dictionary"""
        return word in self.dictionary
    
    def suggest(self, word, n=5, cutoff=0.6):
        """
        Suggest corrections for a word
        
        Args:
            word: Word to check
            n: Number of suggestions
            cutoff: Similarity threshold
            
        Returns:
            List of suggested corrections
        """
        if self.is_correct(word):
            return [word]
        
        # Use difflib to find close matches
        suggestions = get_close_matches(word, self.dictionary, n=n, cutoff=cutoff)
        
        return suggestions
    
    def check_text(self, text):
        """
        Check all words in text
        
        Args:
            text: Text to check
            
        Returns:
            List of tuples (word, is_correct, suggestions)
        """
        tokenizer = NepaliTokenizer()
        words = tokenizer.word_tokenize(text)
        
        results = []
        for word in words:
            is_correct = self.is_correct(word)
            suggestions = [] if is_correct else self.suggest(word, n=3)
            results.append((word, is_correct, suggestions))
        
        return results


if __name__ == "__main__":
    # Test tokenizer
    tokenizer = NepaliTokenizer()
    
    test_text = "नेपाल एक सुन्दर देश हो। काठमाडौं यसको राजधानी हो। तपाईं कहाँ जानुहुन्छ?"
    
    print("Sentence Tokenization:")
    sentences = tokenizer.sentence_tokenize(test_text)
    for i, sent in enumerate(sentences, 1):
        print(f"  {i}. {sent}")
    
    print("\nWord Tokenization:")
    words = tokenizer.word_tokenize(test_text)
    print(f"  Words: {words}")
    
    print("\nN-grams:")
    bigrams = tokenizer.generate_ngrams(words, n=2)
    print(f"  Bigrams (first 5): {bigrams[:5]}")
    
    print("\nStatistics:")
    stats = tokenizer.get_statistics(test_text)
    for key, value in stats.items():
        print(f"  {key}: {value}")
