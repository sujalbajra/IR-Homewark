import re
from .ch02_text_analysis import TextAnalysis

class QueryProcessing:
    def __init__(self, data_dir):
        self.analyzer = TextAnalysis(data_dir)
        
    def levenshtein_distance(self, s1, s2):
        """Compute edit distance for spell correction"""
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def spell_suggest(self, word, dictionary, max_suggestions=3):
        """Simple spell checker using edit distance"""
        distances = [(w, self.levenshtein_distance(word, w)) for w in dictionary]
        distances.sort(key=lambda x: x[1])
        return distances[:max_suggestions]
    
    def wildcard_to_regex(self, pattern):
        """Convert wildcard pattern to regex"""
        if not pattern: return '^$'
        # Replace * with .*
        regex = pattern.replace('*', '.*')
        return f'^{regex}$'
    
    def match_wildcard(self, pattern, terms):
        """Match wildcard pattern against term list"""
        regex_pattern = self.wildcard_to_regex(pattern)
        compiled = re.compile(regex_pattern)
        return [term for term in terms if compiled.match(term)]
