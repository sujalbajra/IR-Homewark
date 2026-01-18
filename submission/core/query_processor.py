
class QueryProcessor:
    def __init__(self, word_analyzer):
        self.analyzer = word_analyzer

    def process_query(self, query):
        """
        Analyze query for entities, intent, and expansion.
        """
        if not query:
            return {}
            
        words = query.split()
        entities = []
        intent = "General Search"
        
        # 1. Extract Entities
        for word in words:
            # Strip punctuation
            clean_word = "".join(c for c in word if c.isalnum())
            analysis = self.analyzer.analyze_word(clean_word)
            if analysis['entity_type']:
                entities.append({
                    'text': clean_word,
                    'type': analysis['entity_type']
                })
        
        # 2. Intent Classification (Simple Rule-based)
        lower_query = query.lower()
        if any(w in lower_query for w in ['ko', 'k', 'who']):
             intent = "Person Factoid"
        elif any(w in lower_query for w in ['kaha', 'where']):
             intent = "Location Factoid"
        elif any(w in lower_query for w in ['kahile', 'when']):
             intent = "Time Factoid"
        elif '?' in query:
             intent = "Question"
             
        # Detect intent based on entities found
        entity_types = [e['type'] for e in entities]
        if 'PER' in entity_types and 'Person' not in intent:
            intent += " (Person-centric)"
        if 'LOC' in entity_types and 'Location' not in intent:
            intent += " (Location-centric)"
            
        return {
            'original': query,
            'entities': entities,
            'intent': intent,
            'tokens': words
        }
