
import hashlib
import random
import re
from .ch02_text_analysis import TextAnalysis

class WebSearch:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.analyzer = TextAnalysis(data_dir)
        
    def _get_shingles(self, text, k=4):
        tokens = self.analyzer.analyze_text(text)['tokens']
        shingles = set()
        for i in range(len(tokens) - k + 1):
            shingle = " ".join(tokens[i:i+k])
            shingles.add(shingle)
        return shingles

    def compute_simhash(self, text, hash_bits=64):
        """
        Computes SimHash fingerprint for text
        """
        shingles = self._get_shingles(text)
        v = [0] * hash_bits
        
        for shingle in shingles:
            # MD5 hash of shingle
            hash_val = int(hashlib.md5(shingle.encode('utf-8')).hexdigest(), 16)
            
            for i in range(hash_bits):
                if (hash_val >> i) & 1:
                    v[i] += 1
                else:
                    v[i] -= 1
                    
        fingerprint = 0
        for i in range(hash_bits):
            if v[i] > 0:
                fingerprint |= (1 << i)
                
        return bin(fingerprint)[2:].zfill(hash_bits)

    def hamming_distance(self, simhash1, simhash2):
        x = int(simhash1, 2) ^ int(simhash2, 2)
        return bin(x).count('1')

    def detect_spam(self, text):
        """
        Heuristic-based spam detection.
        Returns score (0-100) and reasons.
        """
        score = 0
        reasons = []
        
        # 1. Keyword Stuffing Check (Naive)
        tokens = self.analyzer.analyze_text(text)['tokens']
        if len(tokens) == 0:
            return 100, ["Empty content"]
            
        counts = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
            
        top_word, top_count = max(counts.items(), key=lambda x: x[1]) if counts else ("", 0)
        
        # If a single word is > 15% of content
        if top_count / len(tokens) > 0.15:
            score += 40
            reasons.append(f"High keyword density: '{top_word}'")
            
        # 2. Length check
        if len(tokens) < 10:
            score += 20
            reasons.append("Very short content")
            
        # 3. Gibberish check (avg word length)
        avg_len = sum(len(t) for t in tokens) / len(tokens)
        if avg_len > 15:
            score += 30
            reasons.append("Words unusually long (possible gibberish)")
            
        # 4. Link spam simulation (placeholder)
        if "http" in text:
            score += 10
            reasons.append("Contains external links")
            
        return min(score, 100), reasons
