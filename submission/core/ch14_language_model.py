"""
Chapter 14: N-gram Language Model
Implements vanilla Python n-gram LM for Nepali text generation and prediction
"""

from collections import defaultdict, Counter

class NepaliNgramLM:
    """N-gram Language Model for Nepali text"""
    
    def __init__(self, n=2):
        """
        Initialize N-gram Language Model
        
        Args:
            n: N-gram order (2=bigram, 3=trigram)
        """
        self.n = n
        self.ngrams = defaultdict(Counter)  # {context: Counter({word: count})}
        self.context_counts = Counter()      # {context: total_count}
        self.vocabulary = set()
        
    def train(self, sentences):
        """
        Train the language model on a corpus
        
        Args:
            sentences: List of Nepali sentences
        """
        for sent in sentences:
            # Add start/end markers
            words = ['<START>'] * (self.n - 1) + sent.split() + ['<END>']
            self.vocabulary.update(words)
            
            # Count n-grams
            for i in range(len(words) - self.n + 1):
                context = tuple(words[i:i+self.n-1])
                word = words[i+self.n-1]
                
                self.ngrams[context][word] += 1
                self.context_counts[context] += 1
    
    def predict_next(self, context_text, top_k=5):
        """
        Predict next word(s) given context
        
        Args:
            context_text: String of context words
            top_k: Number of predictions to return
            
        Returns:
            List of (word, probability) tuples
        """
        # Extract last n-1 words as context
        words = context_text.split()
        if len(words) < self.n - 1:
            # Pad with START tokens if needed
            context = tuple(['<START>'] * (self.n - 1 - len(words)) + words)
        else:
            context = tuple(words[-(self.n-1):])
        
        if context not in self.ngrams:
            return []
        
        # Calculate probabilities
        candidates = self.ngrams[context]
        total = self.context_counts[context]
        
        predictions = [(word, count/total) for word, count in candidates.most_common(top_k)]
        return predictions
    
    def generate(self, start_text, max_words=20, temperature=1.0):
        """
        Generate text continuation
        
        Args:
            start_text: Seed text to start generation
            max_words: Maximum words to generate
            temperature: Sampling temperature (higher = more random)
            
        Returns:
            Generated text string
        """
        import numpy as np
        
        words = start_text.split() if start_text else ['<START>']
        
        for _ in range(max_words):
            # Get context
            if len(words) < self.n - 1:
                context = tuple(['<START>'] * (self.n - 1 - len(words)) + words)
            else:
                context = tuple(words[-(self.n-1):])
            
            # Get predictions
            predictions = self.predict_next(' '.join(words), top_k=10)
            if not predictions:
                break
            
            # Sample next word (with temperature)
            words_list, probs = zip(*predictions)
            
            # Apply temperature
            probs = np.array(probs)
            probs = np.power(probs, 1.0/temperature)
            probs = probs / probs.sum()
            
            # Sample
            next_word = np.random.choice(words_list, p=probs)
            
            if next_word == '<END>':
                break
            
            words.append(next_word)
        
        # Remove START tokens and return
        result = [w for w in words if w != '<START>']
        return ' '.join(result)
    
    def perplexity(self, test_sentences):
        """
        Calculate perplexity on test data
        
        Args:
            test_sentences: List of test sentences
            
        Returns:
            Perplexity score (lower is better)
        """
        import numpy as np
        
        log_prob_sum = 0
        word_count = 0
        
        for sent in test_sentences:
            words = ['<START>'] * (self.n - 1) + sent.split() + ['<END>']
            
            for i in range(len(words) - self.n + 1):
                context = tuple(words[i:i+self.n-1])
                word = words[i+self.n-1]
                
                if context in self.ngrams and word in self.ngrams[context]:
                    prob = self.ngrams[context][word] / self.context_counts[context]
                    log_prob_sum += np.log(prob)
                else:
                    # Smoothing: assign small probability to unseen n-grams
                    log_prob_sum += np.log(1e-10)
                
                word_count += 1
        
        # Perplexity = exp(-1/N * sum(log(p)))
        avg_log_prob = log_prob_sum / word_count
        perplexity = np.exp(-avg_log_prob)
        
        return perplexity
    
    def get_stats(self):
        """Get model statistics"""
        return {
            'n': self.n,
            'vocab_size': len(self.vocabulary),
            'unique_contexts': len(self.ngrams),
            'total_ngrams': sum(self.context_counts.values())
        }

if __name__ == "__main__":
    # Test with sample Nepali sentences
    train_corpus = [
        "नेपाल एक सुन्दर देश हो",
        "नेपाल हिमालयको देश हो",
        "काठमाडौं नेपालको राजधानी हो"
    ]
    
    # Train bigram model
    lm = NepaliNgramLM(n=2)
    lm.train(train_corpus)
    
    print("✓ Model trained!")
    print(f"Stats: {lm.get_stats()}")
    
    # Test prediction
    context = "नेपाल"
    predictions = lm.predict_next(context)
    print(f"\nPredictions after '{context}':")
    for word, prob in predictions:
        print(f"  {word}: {prob:.3f}")
    
    # Test generation
    generated = lm.generate("नेपाल", max_words=10)
    print(f"\nGenerated text: {generated}")
