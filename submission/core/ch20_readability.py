import re
import math
import os

class NepaliReadability:
    def __init__(self, dictionary_path=None):
        self.FIRST_SYMBOLS = ['ऀ', 'ँ', 'ं', 'ः']
        self.VOWELS = [
            'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ऌ',
            'ऍ', 'ऎ', 'ए', 'ऐ', 'ऑ', 'ऒ', 'ओ', 'औ'
        ]
        self.CONSONANTS = [
            'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ',
            'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न',
            'ऩ', 'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ऱ', 'ल',
            'ळ', 'ऴ', 'व', 'श', 'ष', 'स', 'ह', 'त्र', 'क्ष'
        ]
        self.MATRAS = ["ा", "ि", "ी", "ु", "ू", "ृ", "े", "ै", "ो", "ौ"]
        self.HALANT = '्'
        self.SPLIT_MARKER = '+'
        
        self.known_words = set()
        if dictionary_path and os.path.exists(dictionary_path):
            self._load_dictionary(dictionary_path)

    def _load_dictionary(self, path):
        try:
            import csv
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.known_words.add(row.get('Token', '').strip())
        except Exception as e:
            print(f"Error loading dictionary: {e}")

    def clean_sentence(self, sentence):
        # Remove non-Devanagari characters and extra spaces.
        cleaned_token = re.sub(r'[^\s\u0900-\u097F]', ' ', sentence)
        # Remove sequences like "/ /" or "/ //".
        cleaned_token = re.sub(r'\/\s*\/+', '', cleaned_token)
        # Replace '।' with a space.
        cleaned_token = re.sub(r'।', ' ', cleaned_token)
        # Remove Nepali digits.
        cleaned_token = re.sub(r'[\u0966-\u096F]', '', cleaned_token)
        # Replace multiple spaces with one and trim.
        cleaned_token = re.sub(r'\s+', ' ', cleaned_token).strip()
        return cleaned_token

    def count_letters(self, word):
        vowel_count = 0
        consonant_count = 0
        for char in word:
            if char in self.VOWELS:
                vowel_count += 1
            elif char in self.CONSONANTS:
                consonant_count += 1
        return vowel_count + consonant_count

    def parse_nepali_syllables(self, word):
        syllables = []
        current_syllable = ""
        i = 0
        length = len(word)

        while i < length:
            char = word[i]

            if char in self.VOWELS:
                if current_syllable:
                    syllables.append(current_syllable)
                    current_syllable = ""
                syllables.append(char)
                i += 1

            elif char in self.CONSONANTS:
                current_syllable += char
                i += 1
                if i < length and word[i] == self.HALANT:
                    current_syllable += self.HALANT
                    i += 1
                    if i < length and word[i] in self.CONSONANTS:
                        current_syllable += word[i]
                        i += 1
                    else:
                        pass
                if i < length and word[i] in self.MATRAS:
                    current_syllable += word[i]
                    i += 1
                    syllables.append(current_syllable)
                    current_syllable = ""
                else:
                    syllables.append(current_syllable)
                    current_syllable = ""

            elif char in self.FIRST_SYMBOLS or char in self.MATRAS:
                if current_syllable:
                    current_syllable += char
                else:
                    syllables.append(char)
                i += 1
            else:
                if current_syllable:
                    syllables.append(current_syllable)
                    current_syllable = ""
                syllables.append(char)
                i += 1

        if current_syllable:
            syllables.append(current_syllable)
        return syllables

    def analyze_text(self, text):
        # Split by typical sentence endings
        raw_sentences = re.split(r'[।?!]', text)
        sentences = [s.strip() for s in raw_sentences if s.strip()]
        
        total_words = 0
        total_syllables = 0
        total_letters = 0
        total_difficult_words = 0
        polysyllabic_words = 0
        
        for sent in sentences:
            cleaned = self.clean_sentence(sent)
            words = cleaned.split()
            
            for word in words:
                total_words += 1
                syllables = self.parse_nepali_syllables(word)
                num_syllables = len(syllables)
                total_syllables += num_syllables
                total_letters += self.count_letters(word)
                
                # Difficult word logic
                is_difficult = False
                if self.known_words and word not in self.known_words:
                     # Not in dictionary, assume difficult if long
                     if num_syllables > 3:
                         is_difficult = True
                elif not self.known_words:
                    # No dictionary, rely purely on length
                    if num_syllables > 3:
                        is_difficult = True
                
                if is_difficult:
                    total_difficult_words += 1
                
                if num_syllables >= 3:
                    polysyllabic_words += 1

        stats = {
            'sentences': len(sentences),
            'words': total_words,
            'syllables': total_syllables,
            'letters': total_letters,
            'difficult_words': total_difficult_words,
            'polysyllabic_words': polysyllabic_words
        }
        
        return self._calculate_scores(stats)

    def _calculate_scores(self, stats):
        words = stats['words']
        sentences = stats['sentences']
        syllables = stats['syllables']
        letters = stats['letters']
        difficult_words = stats['difficult_words']
        polysyllabic_words = stats['polysyllabic_words']
        
        if words == 0 or sentences == 0:
            return {'error': 'Not enough text to analyze'}
            
        scores = {}
        
        # Flesch-Kincaid Grade Level
        scores['flesch_kincaid'] = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
        
        # Flesch Reading Ease
        scores['flesch_reading_ease'] = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        
        # Gunning Fog Index
        if words > 0:
            scores['gunning_fog'] = 0.4 * ((words / sentences) + 100 * (difficult_words / words))
        else:
            scores['gunning_fog'] = 0
            
        # Coleman-Liau Index
        L = (letters / words) * 100
        S = (sentences / words) * 100
        scores['coleman_liau'] = 0.0588 * L - 0.296 * S - 15.8
        
        # ARI
        scores['ari'] = 4.71 * (letters / words) + 0.5 * (words / sentences) - 21.43
        
        # SMOG
        scores['smog'] = 1.0430 * (polysyllabic_words * (30 / sentences))**0.5 + 3.1291
        
        stats.update(scores)
        return stats
