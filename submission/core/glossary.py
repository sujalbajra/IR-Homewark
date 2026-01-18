
"""
Glossary of NLP terminology for Nepali language processing.

Provides bilingual (English/Nepali) explanations of linguistic terms,
POS tags, dependency labels, and NER types.
"""

import warnings
from typing import Optional

def explain(term: str) -> Optional[str]:
    """
    Get a bilingual description for a POS tag, dependency label, or NER type.
    """
    if term in GLOSSARY:
        return GLOSSARY[term]
    else:
        # Simple lookup failed, try case insensitive
        for k, v in GLOSSARY.items():
            if k.lower() == term.lower():
                return v
        return None

# =============================================================================
# GLOSSARY: Bilingual NLP Terminology (English + Nepali Devanagari)
# =============================================================================

GLOSSARY = {
    # Universal POS Tags
    "ADJ": "adjective (विशेषण)",
    "ADP": "adposition (कारक चिह्न)",
    "ADV": "adverb (क्रियाविशेषण)",
    "AUX": "auxiliary verb (सहायक क्रिया)",
    "CCONJ": "coordinating conjunction (समानाधिकरण समुच्चयबोधक)",
    "DET": "determiner (निर्धारक)",
    "INTJ": "interjection (विस्मयादिबोधक)",
    "NOUN": "noun (संज्ञा)",
    "NUM": "numeral (संख्यावाचक)",
    "PART": "particle (अव्यय)",
    "PRON": "pronoun (सर्वनाम)",
    "PROPN": "proper noun (व्यक्तिवाचक संज्ञा)",
    "PUNCT": "punctuation (विराम चिह्न)",
    "SCONJ": "subordinating conjunction (व्याधिकरण समुच्चयबोधक)",
    "SYM": "symbol (प्रतीक)",
    "VERB": "verb (क्रिया)",
    "X": "other (अन्य)",
    
    # NER Types
    "PERSON": "person name (व्यक्तिको नाम)",
    "PER": "person name (व्यक्तिको नाम)",
    "LOC": "location (स्थान)",
    "ORG": "organization (संस्था)",
    "GPE": "geo-political entity (भू-राजनीतिक इकाई)",
    "DATE": "date expression (मिति)",
    "TIME": "time expression (समय)",
    "MONEY": "monetary value (मुद्रा)",
    "PERCENT": "percentage (प्रतिशत)",
    "QUANTITY": "quantity (परिमाण)",
    "FACILITY": "facility (सुविधा)",
    "PRODUCT": "product (उत्पादन)",
    "EVENT": "event (घटना)",
    
    # NLP Tasks
    "tokenization": "splitting text into words (शब्द विभाजन)",
    "lemmatization": "finding base form (मूल रूप खोज्ने)",
    "stemming": "removing affixes (प्रत्यय हटाउने)",
    "pos_tagging": "part-of-speech tagging (शब्दवर्ग निर्धारण)",
    "ner": "named entity recognition (नामित संस्था पहिचान)",
    "classification": "text classification (पाठ वर्गीकरण)",
    "translation": "machine translation (मेसिन अनुवाद)",
    "summarization": "text summarization (पाठ सारांश)",
    
    # General Tech
    "embedding": "word vector (शब्द सदिश)",
    "model": "trained system (प्रशिक्षित प्रणाली)",
    "training": "model training (मोडेल प्रशिक्षण)",
    "evaluation": "performance measurement (कार्यसम्पादन मापन)",
    "accuracy": "correctness rate (शुद्धता दर)",
    "precision": "exactness (परिशुद्धता)",
    "recall": "completeness (पूर्णता)",
}
