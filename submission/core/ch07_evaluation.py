import numpy as np
from collections import defaultdict

class Evaluation:
    def __init__(self):
        pass
    
    def precision(self, retrieved, relevant):
        """Precision = |Retrieved ∩ Relevant| / |Retrieved|"""
        if not retrieved:
            return 0.0
        return len(set(retrieved) & set(relevant)) / len(retrieved)
    
    def recall(self, retrieved, relevant):
        """Recall = |Retrieved ∩ Relevant| / |Relevant|"""
        if not relevant:
            return 0.0
        return len(set(retrieved) & set(relevant)) / len(relevant)
    
    def f1_score(self, precision, recall):
        """F1 = 2 * (P * R) / (P + R)"""
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)
    
    def average_precision(self, retrieved, relevant):
        """Average Precision for a single query"""
        if not relevant:
            return 0.0
        
        score = 0.0
        num_hits = 0.0
        
        for i, doc in enumerate(retrieved):
            if doc in relevant:
                num_hits += 1.0
                precision_at_i = num_hits / (i + 1.0)
                score += precision_at_i
        
        return score / len(relevant)
    
    def mean_average_precision(self, results_dict, relevance_dict):
        """MAP across multiple queries"""
        aps = []
        for query_id, retrieved in results_dict.items():
            relevant = relevance_dict.get(query_id, [])
            ap = self.average_precision(retrieved, relevant)
            aps.append(ap)
        
        return np.mean(aps) if aps else 0.0
    
    def dcg(self, relevances):
        """Discounted Cumulative Gain"""
        return sum((2**rel - 1) / np.log2(i + 2) for i, rel in enumerate(relevances))
    
    def ndcg(self, retrieved_relevances, ideal_relevances):
        """Normalized DCG"""
        dcg_score = self.dcg(retrieved_relevances)
        idcg_score = self.dcg(sorted(ideal_relevances, reverse=True))
        
        if idcg_score == 0:
            return 0.0
        return dcg_score / idcg_score
    
    def mrr(self, results_dict, relevance_dict):
        """Mean Reciprocal Rank"""
        reciprocal_ranks = []
        
        for query_id, retrieved in results_dict.items():
            relevant = set(relevance_dict.get(query_id, []))
            for i, doc in enumerate(retrieved):
                if doc in relevant:
                    reciprocal_ranks.append(1.0 / (i + 1))
                    break
            else:
                reciprocal_ranks.append(0.0)
        
        return np.mean(reciprocal_ranks) if reciprocal_ranks else 0.0
