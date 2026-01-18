"""
Chapter 19: Nepali Romanization / Transliteration
Converts Roman text to Nepali Unicode and vice versa
"""

class NepaliRomanization:
    """Romanized input to Nepali Unicode converter"""
    
    # Vowels
    # Vowels (Independent)
    VOWELS = {
        'a': 'अ', 'aa': 'आ', 'i': 'इ', 'ii': 'ई', 'ee': 'ई',
        'u': 'उ', 'uu': 'ऊ', 'oo': 'ऊ',
        'e': 'ए', 'ai': 'ऐ', 
        'o': 'ओ', 'au': 'औ',
        'ri': 'ऋ', 'rri': 'ॠ'
    }
    
    # Consonants (Base forms)
    CONSONANTS = {
        'k': 'क', 'kh': 'ख', 'g': 'ग', 'gh': 'घ', 'ng': 'ङ',
        'ch': 'च', 'chh': 'छ', 'j': 'ज', 'jh': 'झ', 'yn': 'ञ',
        'T': 'ट', 'Th': 'ठ', 'D': 'ड', 'Dh': 'ढ', 'N': 'ण',
        't': 'त', 'th': 'थ', 'd': 'द', 'dh': 'ध', 'n': 'न',
        'p': 'प', 'ph': 'फ', 'b': 'ब', 'bh': 'भ', 'm': 'म',
        'y': 'य', 'r': 'र', 'l': 'ल', 'w': 'व', 'v': 'व',
        'sh': 'श', 'shh': 'ष', 's': 'स', 'h': 'ह',
        'ksh': 'क्ष', 'tr': 'त्र', 'gy': 'ज्ञ',
        'ch': 'च', 'chh': 'छ' # Duplicates handled by order or dict
    }
    
    # Vowel signs (Matras) - 'a' is inherent/schwa (empty string)
    VOWEL_SIGNS = {
        'aa': 'ा', 'a': '', 'i': 'ि', 'ii': 'ी', 'ee': 'ी',
        'u': 'ु', 'uu': 'ू', 'oo': 'ू',
        'e': 'े', 'ai': 'ै',
        'o': 'ो', 'au': 'ौ',
        'ri': 'ृ'
    }
    
    # Special characters
    SPECIAL = {
        'M': 'ं', 'H': 'ः', '~': 'ँ',
        '.': '।', '..': '॥',
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
    }
    
    HALANT = '्'
    
    def romanize_to_nepali(self, text):
        """
        Convert romanized text to Nepali Unicode with improved phonetic matching
        """
        result = []
        i = 0
        n = len(text)
        
        while i < n:
            # 1. Check for Independent Vowels (if at start or after vowel/space)
            # Typically independent vowels appear at start of word.
            # But let's simplify: check simplified logic first.
            
            # 1. Special Characters
            if text[i] in self.SPECIAL:
                result.append(self.SPECIAL[text[i]])
                i += 1
                continue
                
            # 2. Consonants
            matched_cons = False
            # greedy match consonant (up to 4 chars like 'shhh'?)
            for l in range(min(4, n - i), 0, -1):
                chunk = text[i:i+l]
                if chunk in self.CONSONANTS:
                    cons_char = self.CONSONANTS[chunk]
                    i += l
                    matched_cons = True
                    
                    # After consonant, check for vowel sign (matra)
                    matched_matra = False
                    for vl in range(min(3, n - i), 0, -1):
                        v_chunk = text[i:i+vl]
                        if v_chunk in self.VOWEL_SIGNS:
                            matra = self.VOWEL_SIGNS[v_chunk]
                            result.append(cons_char)
                            result.append(matra)
                            i += vl
                            matched_matra = True
                            break
                    
                    if not matched_matra:
                        # No vowel follows -> Inherent 'a'?
                        # Usually implied. 'k' -> 'क'. 'k' + space -> 'क '.
                        # Only if next is consonant, might mean halant in strict sense,
                        # but colloquial typing assumes inherent 'a'.
                        # Halant usually usually requires explicit trailing char or logic.
                        # For 'bad', b -> ब (no matra), d -> द. -> बद.
                        result.append(cons_char)
                    
                    break
            
            if matched_cons:
                continue
                
            # 3. Independent Vowels (if not matched as matra after consonant)
            matched_vowel = False
            for l in range(min(3, n - i), 0, -1):
                chunk = text[i:i+l]
                if chunk in self.VOWELS:
                    result.append(self.VOWELS[chunk])
                    i += l
                    matched_vowel = True
                    break
            
            if matched_vowel:
                continue
                
            # 4. Fallback
            result.append(text[i])
            i += 1
            
        return ''.join(result)
    
    def nepali_to_roman(self, text):
        """
        Convert Nepali Unicode to romanized text (simplified)
        
        Args:
            text: Nepali Unicode text
            
        Returns:
            Approximate romanized text
        """
        # Create reverse mapping
        reverse_vowels = {v: k for k, v in self.VOWELS.items()}
        reverse_consonants = {v: k for k, v in self.CONSONANTS.items()}
        reverse_vowel_signs = {v: k for k, v in self.VOWEL_SIGNS.items()}
        reverse_special = {v: k for k, v in self.SPECIAL.items()}
        
        result = []
        i = 0
        
        while i < len(text):
            char = text[i]
            
            # Check consonant
            if char in reverse_consonants:
                result.append(reverse_consonants[char])
                # Check for vowel sign
                if i + 1 < len(text) and text[i + 1] in reverse_vowel_signs:
                    result.append(reverse_vowel_signs[text[i + 1]])
                    i += 2
                    continue
            # Check vowel
            elif char in reverse_vowels:
                result.append(reverse_vowels[char])
            # Check special
            elif char in reverse_special:
                result.append(reverse_special[char])
            # Check halant
            elif char == self.HALANT:
                pass  # Skip halant
            else:
                result.append(char)
            
            i += 1
        
        return ''.join(result)
    
    def get_examples(self):
        """Get example conversions"""
        examples = [
            ('namaste', 'नमस्ते'),
            ('dhanyabaad', 'धन्यबाद'),
            ('nepaal', 'नेपाल'),
            ('kaThamaDau~', 'काठमाडौं'),
            ('shikshaa', 'शिक्षा'),
            ('bidyaarthii', 'बिद्यार्थी'),
            ('pustaka', 'पुस्तक'),
            ('sarakaara', 'सरकार'),
        ]
        return examples


if __name__ == "__main__":
    # Test the romanization
    converter = NepaliRomanization()
    
    print("=== Romanization Examples ===")
    examples = converter.get_examples()
    for roman, expected in examples:
        result = converter.romanize_to_nepali(roman)
        status = "✓" if result == expected else "✗"
        print(f"{status} {roman} → {result} (expected: {expected})")
    
    print("\n=== Custom Tests ===")
    tests = [
        "namaste",
        "dhanyabaad",
        "ma nepaalii hu",
        "ramro chaH",
    ]
    
    for test in tests:
        result = converter.romanize_to_nepali(test)
        print(f"{test} → {result}")
    
    print("\n=== Reverse (Nepali to Roman) ===")
    nepali_text = "नमस्ते"
    roman = converter.nepali_to_roman(nepali_text)
    print(f"{nepali_text} → {roman}")
