"""
Chapter 18: Nepali Number Utilities
Converts numbers between English and Nepali formats
"""

class NepaliNumber:
    """Utility class for Nepali number operations"""
    
    # English to Nepali digit mapping
    NEPALI_DIGITS = {
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
    }
    
    # Nepali to English digit mapping (reverse)
    ENGLISH_DIGITS = {v: k for k, v in NEPALI_DIGITS.items()}
    
    # Nepali words for numbers
    ONES = ['', 'एक', 'दुई', 'तीन', 'चार', 'पाँच', 'छ', 'सात', 'आठ', 'नौ']
    TENS = ['', '', 'बीस', 'तीस', 'चालीस', 'पचास', 'साठी', 'सत्तरी', 'असी', 'नब्बे']
    TEENS = ['दश', 'एघार', 'बाह्र', 'तेह्र', 'चौध', 'पन्ध्र', 'सोह्र', 'सत्र', 'अठार', 'उन्नाइस']
    
    # Place values
    HUNDRED = 'सय'
    THOUSAND = 'हजार'
    LAKH = 'लाख'
    CRORE = 'करोड'
    
    def to_nepali_digits(self, number):
        """
        Convert English digits to Nepali digits
        
        Args:
            number: Number or string with English digits
            
        Returns:
            String with Nepali digits
        """
        text = str(number)
        return ''.join(self.NEPALI_DIGITS.get(char, char) for char in text)
    
    def to_english_digits(self, nepali_text):
        """
        Convert Nepali digits to English digits
        
        Args:
            nepali_text: String with Nepali digits
            
        Returns:
            String with English digits
        """
        return ''.join(self.ENGLISH_DIGITS.get(char, char) for char in nepali_text)
    
    def to_nepali_words(self, number):
        """
        Convert number to Nepali words
        
        Args:
            number: Integer number (up to 9,99,99,999)
            
        Returns:
            Number in Nepali words
        """
        if not isinstance(number, int) or number < 0:
            return ""
        
        if number == 0:
            return "शून्य"
        
        # Split into place values (Indian system: crores, lakhs, thousands)
        crores = number // 10000000
        remainder = number % 10000000
        
        lakhs = remainder // 100000
        remainder = remainder % 100000
        
        thousands = remainder // 1000
        remainder = remainder % 1000
        
        hundreds = remainder // 100
        tens_ones = remainder % 100
        
        # Build the word representation
        parts = []
        
        if crores > 0:
            parts.append(self._convert_two_digits(crores) + ' ' + self.CRORE)
        
        if lakhs > 0:
            parts.append(self._convert_two_digits(lakhs) + ' ' + self.LAKH)
        
        if thousands > 0:
            parts.append(self._convert_two_digits(thousands) + ' ' + self.THOUSAND)
        
        if hundreds > 0:
            parts.append(self.ONES[hundreds] + ' ' + self.HUNDRED)
        
        if tens_ones > 0:
            parts.append(self._convert_two_digits(tens_ones))
        
        return ' '.join(parts).strip()
    
    def _convert_two_digits(self, number):
        """Convert a two-digit number (0-99) to Nepali words"""
        if number == 0:
            return ""
        elif number < 10:
            return self.ONES[number]
        elif 10 <= number < 20:
            return self.TEENS[number - 10]
        else:
            tens_digit = number // 10
            ones_digit = number % 10
            
            if ones_digit == 0:
                return self.TENS[tens_digit]
            else:
                return self.TENS[tens_digit] + ' ' + self.ONES[ones_digit]
    
    def format_with_commas(self, number, use_nepali_digits=True):
        """
        Format number with Indian-style comma separators
        
        Args:
            number: Number to format
            use_nepali_digits: Use Nepali digits if True
            
        Returns:
            Formatted string (e.g., 1,23,456 or १,२३,४५६)
        """
        # Convert to string
        num_str = str(number)
        
        # Handle decimal point
        if '.' in num_str:
            integer_part, decimal_part = num_str.split('.')
        else:
            integer_part = num_str
            decimal_part = None
        
        # Apply Indian comma formatting
        if len(integer_part) <= 3:
            formatted = integer_part
        else:
            # Last 3 digits
            formatted = integer_part[-3:]
            remaining = integer_part[:-3]
            
            # Add commas every 2 digits from right
            while remaining:
                if len(remaining) <= 2:
                    formatted = remaining + ',' + formatted
                    break
                else:
                    formatted = remaining[-2:] + ',' + formatted
                    remaining = remaining[:-2]
        
        # Add decimal part back
        if decimal_part:
            formatted += '.' + decimal_part
        
        # Convert to Nepali digits if requested
        if use_nepali_digits:
            formatted = self.to_nepali_digits(formatted)
        
        return formatted


if __name__ == "__main__":
    # Test the converter
    converter = NepaliNumber()
    
    print("=== Digit Conversion ===")
    print(f"123 → {converter.to_nepali_digits(123)}")
    print(f"456789 → {converter.to_nepali_digits(456789)}")
    print(f"१२३४५६ → {converter.to_english_digits('१२३४५६')}")
    
    print("\n=== Number to Words ===")
    test_numbers = [0, 5, 15, 23, 100, 456, 1234, 12345, 123456, 1234567]
    for num in test_numbers:
        print(f"{num} → {converter.to_nepali_words(num)}")
    
    print("\n=== Comma Formatting ===")
    print(f"1234567 → {converter.format_with_commas(1234567)}")
    print(f"1234567 (English) → {converter.format_with_commas(1234567, use_nepali_digits=False)}")
    print(f"123456789.50 → {converter.format_with_commas(123456789.50)}")
