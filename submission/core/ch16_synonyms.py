"""
Chapter 16: Synonym Finder
Uses dummy word embeddings to find similar words via cosine similarity
"""

import numpy as np

class NepaliSynonyms:
    """Find synonyms using word embeddings and cosine similarity"""
    
    def __init__(self, embeddings_path='data/nepali_embeddings.npz'):
        """
        Initialize synonym finder with embeddings
        
        Args:
            embeddings_path: Path to embeddings file
        """
        self.vocab = {}
        self.embeddings = None
        self.word_to_idx = {}
        self.idx_to_word = {}
        
        self.load_embeddings(embeddings_path)
    
    def load_embeddings(self, path):
        """Load word embeddings from file"""
        try:
            data = np.load(path, allow_pickle=True)
            # embeddings is saved as a dict inside 0-d array
            self.embeddings = data['embeddings'].item()
            
            # Vocab comes directly from keys
            self.vocab = list(self.embeddings.keys())
            
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            # Initialize empty
            self.vocab = []
            self.embeddings = {}
    
    def cosine_similarity(self, vec1, vec2):
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vec1, vec2: Numpy arrays
            
        Returns:
            Similarity score (0-1)
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def find_synonyms(self, word, top_k=5):
        """
        Find most similar words to given word
        
        Args:
            word: Word to find synonyms for
            top_k: Number of synonyms to return
            
        Returns:
            List of (word, similarity_score) tuples
        """
    def find_synonyms(self, word, top_k=5):
        """
        Find most similar words to given word
        
        Args:
            word: Word to find synonyms for
            top_k: Number of synonyms to return
            
        Returns:
            List of (word, similarity_score) tuples
        """
        if word not in self.embeddings:
            return []
        
        word_vec = self.embeddings[word]
        
        # Calculate similarity with all other words
        similarities = []
        for other_word, other_vec in self.embeddings.items():
            if other_word == word:
                continue  # Skip the word itself
            
            sim = self.cosine_similarity(word_vec, other_vec)
            similarities.append((other_word, float(sim)))
        
        # Sort by similarity (descending) and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def word_similarity(self, word1, word2):
        """
        Calculate similarity between two specific words
        
        Args:
            word1, word2: Words to compare
            
        Returns:
            Similarity score (0-1)
        """
        if word1 not in self.word_to_idx or word2 not in self.word_to_idx:
            return 0.0
        
        vec1 = self.embeddings[self.word_to_idx[word1]]
        vec2 = self.embeddings[self.word_to_idx[word2]]
        
        return self.cosine_similarity(vec1, vec2)
    
    def get_vocabulary(self):
        """Get list of all words in vocabulary"""
        return self.vocab


if __name__ == "__main__":
    # Test synonym finder
    finder = NepaliSynonyms()
    
    print(f"Vocabulary size: {len(finder.get_vocabulary())}")
    print(f"\nSample words: {finder.get_vocabulary()[:10]}")
    
    test_word = "नेपाल"
    if test_word in finder.vocab:
        synonyms = finder.find_synonyms(test_word, top_k=5)
        print(f"\nTop 5 synonyms for '{test_word}':")
        for word, sim in synonyms:
            print(f"  {word}: {sim:.4f}")
