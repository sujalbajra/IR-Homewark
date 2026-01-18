
from collections import Counter

class BiasDetector:
    def __init__(self):
        self.male_terms = {'he', 'him', 'his', 'man', 'men', 'boy', 'boys', 'father', 'brother'}
        self.female_terms = {'she', 'her', 'hers', 'woman', 'women', 'girl', 'girls', 'mother', 'sister'}
        
    def analyze_text(self, text):
        """
        Analyze text for gender bias.
        Returns: {
            'male_count': int,
            'female_count': int,
            'bias_score': float (-1 to 1, where -1 is female biased, 1 is male biased, 0 is neutral),
            'verdict': str
        }
        """
        words = text.lower().split()
        counts = Counter(words)
        
        m_count = sum(counts[t] for t in self.male_terms if t in counts)
        f_count = sum(counts[t] for t in self.female_terms if t in counts)
        
        total = m_count + f_count
        score = 0.0
        
        if total > 0:
            score = (m_count - f_count) / total
            
        verdict = "Neutral"
        if score > 0.2:
            verdict = "Male Leaning"
        elif score < -0.2:
            verdict = "Female Leaning"
            
        return {
            'male_count': m_count,
            'female_count': f_count,
            'bias_score': round(score, 2),
            'verdict': verdict
        }

    def analyze_corpus(self, documents):
        """
        Analyze list of document texts.
        """
        total_m = 0
        total_f = 0
        
        for doc in documents.values():
            res = self.analyze_text(doc)
            total_m += res['male_count']
            total_f += res['female_count']
            
        total = total_m + total_f
        score = (total_m - total_f) / total if total > 0 else 0
        
        return {
            'collection_male': total_m,
            'collection_female': total_f,
            'collection_bias': round(score, 2)
        }
