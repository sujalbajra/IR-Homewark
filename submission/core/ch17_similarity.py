"""
Chapter 17: Sentence Similarity
Implements three similarity metrics: Jaccard, Cosine, and Edit Distance
"""

import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.ch15_tokenization import NepaliTokenizer

class NepaliSimilarity:
    """Sentence similarity using multiple methods"""
    
    def __init__(self, embeddings_path='data/nepali_embeddings.npz'):
        """Initialize with tokenizer and embeddings"""
        self.tokenizer = NepaliTokenizer()
        self.vocab = {}
        self.embeddings = None
        
        # Load embeddings
        try:
            data = np.load(embeddings_path, allow_pickle=True)
            self.embeddings = data['embeddings'].item()
            self.vocab = list(self.embeddings.keys())
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            pass
    
    def jaccard_similarity(self, sent1, sent2):
        """
        Calculate Jaccard similarity (token overlap)
        
        Args:
            sent1, sent2: Sentences to compare
            
        Returns:
            Similarity score (0-1)
        """
        # Tokenize
        tokens1 = set(self.tokenizer.word_tokenize(sent1))
        tokens2 = set(self.tokenizer.word_tokenize(sent2))
        
        if not tokens1 and not tokens2:
            return 1.0
        
        # Jaccard = |intersection| / |union|
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def cosine_similarity(self, sent1, sent2):
        """
        Calculate cosine similarity using average word embeddings
        
        Args:
            sent1, sent2: Sentences to compare
            
        Returns:
            Similarity score (0-1)
        """
        if self.embeddings is None:
            return 0.0
        
        # Get average embedding for each sentence
        vec1 = self._get_sentence_vector(sent1)
        vec2 = self._get_sentence_vector(sent2)
        
        if vec1 is None or vec2 is None:
            return 0.0
        
        # Cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _get_sentence_vector(self, sentence):
        """Get average embedding vector for a sentence"""
        words = self.tokenizer.word_tokenize(sentence)
        vectors = []
        
        for word in words:
            if word in self.embeddings:
                vectors.append(self.embeddings[word])
        
        if not vectors:
            return None
        
        # Average all word vectors
        return np.mean(vectors, axis=0)
    
    def edit_distance(self, sent1, sent2):
        """
        Calculate Levenshtein edit distance at word level
        
        Args:
            sent1, sent2: Sentences to compare
            
        Returns:
            Edit distance (number of operations needed)
        """
        words1 = self.tokenizer.word_tokenize(sent1)
        words2 = self.tokenizer.word_tokenize(sent2)
        
        return self._levenshtein(words1, words2)
    
    def _levenshtein(self, seq1, seq2):
        """Levenshtein distance implementation"""
        if len(seq1) < len(seq2):
            return self._levenshtein(seq2, seq1)
        
        if len(seq2) == 0:
            return len(seq1)
        
        previous_row = list(range(len(seq2) + 1))
        
        for i, item1 in enumerate(seq1):
            current_row = [i + 1]
            for j, item2 in enumerate(seq2):
                # Cost of insertions, deletions, or substitutions
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (item1 != item2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def edit_similarity(self, sent1, sent2):
        """
        Normalized edit similarity (1 - normalized_distance)
        
        Returns:
            Similarity score (0-1)
        """
        words1 = self.tokenizer.word_tokenize(sent1)
        words2 = self.tokenizer.word_tokenize(sent2)
        
        max_len = max(len(words1), len(words2))
        if max_len == 0:
            return 1.0
        
        distance = self._levenshtein(words1, words2)
        return 1.0 - (distance / max_len)
    
    def compare_all(self, sent1, sent2):
        """
        Compare two sentences using all metrics
        
        Returns:
            Dictionary with all similarity scores
        """
        return {
            'jaccard': self.jaccard_similarity(sent1, sent2),
            'cosine': self.cosine_similarity(sent1, sent2),
            'edit_distance': self.edit_distance(sent1, sent2),
            'edit_similarity': self.edit_similarity(sent1, sent2)
        }


if __name__ == "__main__":
    # Test similarity
    similarity = NepaliSimilarity()
    
    sent1 = "नेपाल एक सुन्दर देश हो"
    sent2 = "नेपाल धेरै राम्रो देश हो"
    
    print(f"Sentence 1: {sent1}")
    print(f"Sentence 2: {sent2}")
    print("\nSimilarity Scores:")
    
    scores = similarity.compare_all(sent1, sent2)
    for metric, score in scores.items():
        print(f"  {metric}: {score:.4f}")
