
import numpy as np
import torch
import torch.nn as nn
from .ch02_text_analysis import TextAnalysis

class NeuralIR:
    def __init__(self, data_dir):
        self.analyzer = TextAnalysis(data_dir)
        # Mock embeddings for Nepali words (In real world, load GloVe/Word2Vec/BERT)
        self.embedding_dim = 10
        self.vocab = {}
        self.embeddings = {}
        # Pre-seed with some common tokens
        self._init_mock_model()
        
    def _init_mock_model(self):
        # Try loading real embeddings first
        emb_path = os.path.join(self.analyzer.data_dir, 'nepali_embeddings.npz')
        if os.path.exists(emb_path):
            try:
                # Load real data (allow_pickle=True needed for object arrays if any)
                data = np.load(emb_path, allow_pickle=True)
                
                # Check for various key formats (words/vocab, embeddings/vectors)
                words = None
                if 'words' in data: words = data['words']
                elif 'vocab' in data: words = data['vocab']
                
                vecs = None
                if 'embeddings' in data: vecs = data['embeddings']
                elif 'vectors' in data: vecs = data['vectors']
                
                if words is not None and vecs is not None:
                    # Create vocab mapping
                    self.vocab = {w: i for i, w in enumerate(words)}
                    
                    # Initialize embedding layer with real weights
                    # Convert to torch tensor
                    weights = torch.FloatTensor(vecs)
                    self.embedding_dim = weights.shape[1]
                    self.emb_layer = nn.Embedding.from_pretrained(weights)
                    self.embeddings_loaded = True
                    print(f"Loaded real embeddings: {len(words)} words, {self.embedding_dim} dim")
                    return
            except Exception as e:
                print(f"Failed to load embeddings: {e}. Reverting to mock.")

        # Fallback to Mock
        # Deterministic random for demo stability
        torch.manual_seed(42)
        
        # Simulated pre-trained embeddings
        common_terms = ['nepal', 'government', 'development', 'politics', 'sports', 'kathmandu']
        self.vocab = {word: i for i, word in enumerate(common_terms)}
        
        # Random embeddings
        self.emb_layer = nn.Embedding(len(common_terms) + 100, self.embedding_dim) 
        
    def get_embedding(self, text):
        """Get vector representation for text (Average Word Embeddings)"""
        # Improved tokenization handling
        tokens = text.lower().split() # Simple split usually better for embeddings lookups than aggressive stemming
        vectors = []
        
        for token in tokens:
            idx = -1
            if token in self.vocab:
                idx = self.vocab[token]
                vec = self.emb_layer(torch.tensor([idx]))
            else:
                # OOV Strategy:
                # 1. Try stemmed
                stem = self.analyzer.analyze_text(token)['stemmed'][0] if self.analyzer else token
                if stem in self.vocab:
                    idx = self.vocab[stem]
                    vec = self.emb_layer(torch.tensor([idx]))
                else:
                    # 2. Hash trick (fallback)
                    idx = hash(token) % 100 
                    vec = self.emb_layer(torch.tensor([idx]))
            
            vectors.append(vec.detach().numpy())
            
        if not vectors:
            return np.zeros(self.embedding_dim)
            
        return np.mean(vectors, axis=0)

    def dense_retrieval(self, query, docs):
        """
        Compute similarity using dense vectors (simple dot product)
        """
        query_vec = self.get_embedding(query)
        scores = []
        
        for doc_id, text in docs.items():
            doc_vec = self.get_embedding(text)
            
            # Cosine Similarity manually with Numpy
            norm_q = np.linalg.norm(query_vec)
            norm_d = np.linalg.norm(doc_vec)
            
            if norm_q * norm_d == 0:
                score = 0
            else:
                score = np.dot(query_vec.flatten(), doc_vec.flatten()) / (norm_q * norm_d)
                
            scores.append((doc_id, float(score)))
            
        return sorted(scores, key=lambda x: x[1], reverse=True)

    def mock_rag_generation(self, query, top_docs):
        """
        Simulate RAG (Retrieval Augmented Generation) response
        """
        # In a real system, this calls an LLM api
        if not top_docs:
            return "No documents found to generate answer."
        context = " ".join([d[0] for d in top_docs[:2]])
        return f"Based on '{context}', the answer about '{query}' involves simulated neural generation."

    def neural_rerank(self, query, initial_results, doc_texts):
        """
        Re-rank top-k results from initial retrieval using dense vectors.
        initial_results: list of (doc_id, score) tuples
        doc_texts: dict mapping doc_id to text content
        """
        query_vec = self.get_embedding(query)
        reranked_scores = []
        
        for doc_id, original_score in initial_results:
            if doc_id not in doc_texts:
                continue
                
            text = doc_texts[doc_id]
            doc_vec = self.get_embedding(text)
            
            # Compute semantic similarity
            norm_q = np.linalg.norm(query_vec)
            norm_d = np.linalg.norm(doc_vec)
            
            semantic_score = 0
            if norm_q * norm_d > 0:
                semantic_score = np.dot(query_vec.flatten(), doc_vec.flatten()) / (norm_q * norm_d)
                
            # Combine scores: 0.3 * BM25 + 0.7 * Neural
            # Note: Scores should be normalized ideally. Here we just take weighted sum.
            # Assuming original_score is BM25 ~ 10-20. Semantic is 0-1.
            # Let's scale semantic by 10
            final_score = (0.2 * original_score) + (0.8 * semantic_score * 10)
            
            reranked_scores.append((doc_id, float(final_score)))
            
        return sorted(reranked_scores, key=lambda x: x[1], reverse=True)
