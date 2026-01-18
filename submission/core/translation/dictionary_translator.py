
class DictionaryTranslator:
    def __init__(self):
        # Dummy Dictionary (English -> Nepali)
        self.en_to_ne = {
            'government': 'सरकार',
            'development': 'विकास',
            'sports': 'खेलकुद',
            'politics': 'राजनीति',
            'education': 'शिक्षा',
            'health': 'स्वास्थ्य',
            'economy': 'अर्थतन्त्र',
            'agriculture': 'कृषि',
            'tourism': 'पर्यटन',
            'culture': 'संस्कृति',
            'kathmandu': 'काठमाडौँ',
            'nepal': 'नेपाल'
        }

    def translate_query(self, query):
        """
        Simple word-by-word translation.
        """
        words = query.lower().split()
        translated_words = []
        
        for word in words:
            # Check dictionary
            if word in self.en_to_ne:
                translated_words.append(self.en_to_ne[word])
            else:
                # Keep original if not found (or maybe apply transliteration logic in future)
                translated_words.append(word)
                
        return " ".join(translated_words)
