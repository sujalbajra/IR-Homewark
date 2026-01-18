# NER Data - Vocabulary Files

This directory contains clean, deduplicated vocabulary extracted from NER (Named Entity Recognition) data sources.

## 📁 Directory Contents

### Vocabulary Files by Tag

Individual vocabulary files for each entity/content type:

- **PER_vocab.txt** - 2,336 unique person names
- **LOC_vocab.txt** - 1,013 unique locations
- **ORG_vocab.txt** - 1,327 unique organizations
- **GENERAL_vocab.txt** - 2,435 unique general content words
- **PROFANITY_vocab.txt** - 258 unique profanity terms
- **VIOLENCE_vocab.txt** - 358 unique violence-related words
- **FEEDBACK_vocab.txt** - 557 unique feedback/suggestion words
- **MISC_vocab.txt** - 375 unique miscellaneous entities
- **O_vocab.txt** - 17,087 unique non-entity words

### Combined Vocabulary

- **combined_vocab.txt** - 22,240 unique words from all tags (alphabetically sorted)

### Documentation

- **README.md** - This file
- **VOCABULARY_SUMMARY.md** - Detailed summary with statistics and usage examples
- **vocab_statistics.txt** - Statistical breakdown by tag
- **tag_summary.txt** - Original tag analysis from source files

## 📊 Quick Statistics

| Metric | Count |
|--------|-------|
| **Total unique words** | 22,240 |
| **Source files processed** | 2 (nerdata.txt + total.conll) |
| **Original entries** | 162,838 |
| **Duplicates removed** | 84% |
| **Tags identified** | 9 |

## 🎯 File Format

All vocabulary files are plain text files with:
- **One word per line**
- **UTF-8 encoding** (supports Devanagari script)
- **Alphabetically sorted**
- **No duplicates**

## 💡 Usage Examples

### Loading a vocabulary file (Python)

```python
# Load person names vocabulary
with open('PER_vocab.txt', 'r', encoding='utf-8') as f:
    person_names = [line.strip() for line in f]

print(f"Loaded {len(person_names)} unique person names")
```

### Using for NER training

```python
# Create a vocabulary set for quick lookup
vocab = set()
for tag in ['PER', 'LOC', 'ORG']:
    with open(f'{tag}_vocab.txt', 'r', encoding='utf-8') as f:
        vocab.update(line.strip() for line in f)

# Check if a word is an entity
def is_entity(word):
    return word in vocab
```

### Content filtering

```python
# Load profanity vocabulary for content moderation
with open('PROFANITY_vocab.txt', 'r', encoding='utf-8') as f:
    profanity_list = set(line.strip() for line in f)

def filter_text(text):
    words = text.split()
    return ' '.join(w if w not in profanity_list else '***' for w in words)
```

## 📖 Data Sources

The vocabulary was extracted and deduplicated from two NER data sources:

1. **nerdata.txt** - Standard NER format with tags: PER, LOC, ORG, O
2. **total.conll** - CoNLL format with extended tags including content classification

Both sources were combined to provide maximum vocabulary coverage.

## 🔍 Tag Descriptions

| Tag | Description | Count |
|-----|-------------|-------|
| **PER** | Person names (individuals, characters) | 2,336 |
| **LOC** | Locations (cities, countries, landmarks) | 1,013 |
| **ORG** | Organizations (companies, institutions) | 1,327 |
| **GENERAL** | General content/negative sentiment | 2,435 |
| **PROFANITY** | Profane or offensive language | 258 |
| **VIOLENCE** | Violence-related content | 358 |
| **FEEDBACK** | Feedback and suggestions | 557 |
| **MISC** | Miscellaneous entities | 375 |
| **O** | Other non-entity words | 17,087 |

## 📚 Use Cases

These vocabulary files can be used for:

- ✅ **NER Model Training** - Train entity recognition models
- ✅ **Text Classification** - Classify content by entity types
- ✅ **Content Moderation** - Filter inappropriate content
- ✅ **Data Augmentation** - Generate synthetic training data
- ✅ **Feature Engineering** - Create NLP features
- ✅ **Dictionary Building** - Build domain-specific dictionaries
- ✅ **Language Analysis** - Study language patterns and usage

## 🛠️ Processing Details

The vocabulary was created through:
1. **Extraction** - Words extracted from both source files
2. **Combination** - Data from both sources merged
3. **Deduplication** - Duplicates removed (84% reduction)
4. **Sorting** - Alphabetical ordering in Unicode/Devanagari order
5. **Quality Check** - Verification and validation

## 📄 License

This data is derived from publicly available NER datasets. Please refer to the original source licenses for usage terms.

---

For detailed statistics and analysis, see **VOCABULARY_SUMMARY.md**
