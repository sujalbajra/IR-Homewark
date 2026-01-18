# Unique Vocabulary Summary

This document summarizes the unique vocabulary extraction from NER data sources.

## Overview

Successfully created unique vocabulary files by combining and deduplicating entries from both `nerdata.txt` and `total.conll` sources.

## Statistics

### Overall Summary

| Metric | Count |
|--------|-------|
| **Total words (with duplicates)** | 162,838 |
| **Unique words across all tags** | 25,746 |
| **Duplicates removed within tags** | 137,092 |
| **Unique words in combined vocab** | 22,240 |
| **Cross-tag duplicates removed** | 3,506 |

### Breakdown by Tag

| Tag | NERData | CoNLL | Total | Unique | Duplicates Removed |
|-----|---------|-------|-------|--------|---------------------|
| **PER** | 5,956 | 2,885 | 8,841 | 2,336 | 6,505 |
| **LOC** | 3,133 | 446 | 3,579 | 1,013 | 2,566 |
| **ORG** | 5,145 | 419 | 5,564 | 1,327 | 4,237 |
| **GENERAL** | 0 | 5,745 | 5,745 | 2,435 | 3,310 |
| **PROFANITY** | 0 | 743 | 743 | 258 | 485 |
| **VIOLENCE** | 0 | 690 | 690 | 358 | 332 |
| **FEEDBACK** | 0 | 1,101 | 1,101 | 557 | 544 |
| **MISC** | 0 | 1,226 | 1,226 | 375 | 851 |
| **O** | 84,803 | 50,546 | 135,349 | 17,087 | 118,262 |
| **TOTAL** | 99,037 | 63,801 | 162,838 | 25,746 | 137,092 |

## Output Files

### Individual Tag Vocabularies

Each tag has its own vocabulary file containing unique words for that specific entity type:

1. **PER_vocab.txt** - 2,336 unique person names
2. **LOC_vocab.txt** - 1,013 unique locations
3. **ORG_vocab.txt** - 1,327 unique organizations
4. **GENERAL_vocab.txt** - 2,435 unique general content words
5. **PROFANITY_vocab.txt** - 258 unique profanity terms
6. **VIOLENCE_vocab.txt** - 358 unique violence-related words
7. **FEEDBACK_vocab.txt** - 557 unique feedback/suggestion words
8. **MISC_vocab.txt** - 375 unique miscellaneous entities
9. **O_vocab.txt** - 17,087 unique non-entity words

### Combined Vocabulary

**combined_vocab.txt** - Contains 22,240 unique words from all tags combined (alphabetically sorted)

## Key Insights

1. **High Duplication Rate**: 84% of words were duplicates within their respective tags
   - This shows significant overlap between the two source files

2. **Cross-Tag Overlap**: 3,506 words appear in multiple entity categories
   - This is expected as some words can serve different roles in different contexts

3. **O Tag Dominance**: The "O" (non-entity) tag contains 66% of all unique words
   - This represents the general vocabulary used in the text

4. **Source Complementarity**:
   - `nerdata.txt` is strong in traditional NER tags (PER, LOC, ORG)
   - `total.conll` adds content classification categories (GENERAL, PROFANITY, VIOLENCE, FEEDBACK, MISC)

## File Format

All vocabulary files are plain text files with one word per line, sorted alphabetically in Devanagari/Unicode order.

## Usage Examples

These clean vocabulary files can be used for:

- **NER Model Training**: Use tag-specific vocabularies to train entity recognition models
- **Text Classification**: Use category vocabularies (PROFANITY, VIOLENCE) for content filtering
- **Dictionary Creation**: Build specialized dictionaries for different entity types
- **Data Augmentation**: Generate synthetic NER training data
- **Vocabulary Analysis**: Study language patterns in different entity categories
- **Feature Engineering**: Create features based on presence of specific entity types

## Data Quality

✅ **Cleaned**: All entries are deduplicated
✅ **Sorted**: Alphabetically ordered for easy lookup
✅ **Combined**: Both sources merged for maximum coverage
✅ **Organized**: Separate files for each tag type
✅ **Documented**: Complete statistics and metadata provided
