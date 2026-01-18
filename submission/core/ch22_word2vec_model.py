
import numpy as np
import pickle
import os
from .ch02_text_analysis import TextAnalysis

class Word2VecNumPy:
    def __init__(self, vocab_size=5000, embedding_dim=100, learning_rate=0.01):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.lr = learning_rate
        self.w1 = None  # Input to Hidden (Embeddings)
        self.w2 = None  # Hidden to Output
        self.vocab = {}
        self.kv = {}    # Key-Value store for embeddings (like Gensim)
        
    def build_vocab(self, corpus):
        """Build vocabulary from list of text documents"""
        word_counts = {}
        for text in corpus:
            tokens = text.split()
            for token in tokens:
                word_counts[token] = word_counts.get(token, 0) + 1
                
        # Sort by frequency and cut off
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        self.vocab = {w: i for i, (w, _) in enumerate(sorted_words[:self.vocab_size])}
        self.idx_to_word = {i: w for w, i in self.vocab.items()}
        self.actual_vocab_size = len(self.vocab)
        
    def _softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def train(self, corpus, window_size=2, epochs=5):
        """Train Skip-gram model"""
        if not self.vocab:
            self.build_vocab(corpus)
            
        # Initialize weights
        np.random.seed(42)
        self.w1 = np.random.uniform(-0.1, 0.1, (self.actual_vocab_size, self.embedding_dim))
        self.w2 = np.random.uniform(-0.1, 0.1, (self.embedding_dim, self.actual_vocab_size))
        
        history = []
        
        for epoch in range(epochs):
            loss = 0
            for text in corpus:
                tokens = [t for t in text.split() if t in self.vocab]
                for i, target_word in enumerate(tokens):
                    target_idx = self.vocab[target_word]
                    
                    # Context window
                    context_indices = []
                    for j in range(max(0, i - window_size), min(len(tokens), i + window_size + 1)):
                        if i != j:
                            context_idx = self.vocab[tokens[j]]
                            context_indices.append(context_idx)
                            
                    # Simple SGD per context (simplified for educational clarity)
                    for context_idx in context_indices:
                        # Forward
                        h = self.w1[target_idx]
                        u = np.dot(h, self.w2)
                        y_pred = self._softmax(u)
                        
                        # Error
                        e = y_pred.copy()
                        e[context_idx] -= 1
                        
                        # Backprop
                        dw2 = np.outer(h, e)
                        dw1 = np.dot(self.w2, e)
                        
                        self.w2 -= self.lr * dw2
                        self.w1[target_idx] -= self.lr * dw1
                        
                        loss -= np.log(y_pred[context_idx])
                        
            epoch_loss = loss / len(corpus)
            history.append(epoch_loss)
            print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss:.4f}")
            
        # Store final embeddings
        for word, idx in self.vocab.items():
            self.kv[word] = self.w1[idx]
            
        return history

    def save_model(self, path):
        with open(path, 'wb') as f:
            pickle.dump({'vocab': self.vocab, 'w1': self.w1, 'kv': self.kv}, f)

    def load_model(self, path):
        if not os.path.exists(path):
            return False
            
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.vocab = data['vocab']
            self.w1 = data['w1']
            self.kv = data['kv']
            self.idx_to_word = {i: w for w, i in self.vocab.items()}
            return True

    def most_similar(self, word, top_k=5):
        if word not in self.kv:
            return []
            
        vec = self.kv[word]
        scores = []
        
        norm_v = np.linalg.norm(vec)
        
        for w, v in self.kv.items():
            if w == word: continue
            
            norm_w = np.linalg.norm(v)
            if norm_w == 0 or norm_v == 0:
                sim = 0
            else:
                sim = np.dot(vec, v) / (norm_v * norm_w)
                
            scores.append((w, float(sim)))
            
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
