# CSV Corpus Import & Management

This README explains how to import and manage CSV corpora in the IR platform.

## Quick Start

### Import CSV Files
```bash
# From submission directory
python utils/csv_importer.py
```

This will:
1. Import `train.csv` (5,975 documents)
2. Import `valid.csv` (1,495 documents)
3. Update `data/metadata.json`
4. Create `.txt` files in `data/documents/`

## CSV File Format

Your CSV files should have these columns:

| Column | Description |
|--------|-------------|
| `headings` | Document title/heading |
| `paras` | Main paragraph/content |
| `label` | Category label |

Example:
```csv
headings,paras,label
"नेपाली समाचार","यहाँ समाचार सामग्री...",business
"खेल समाचार","क्रिकेट खेलमा...",sports
```

## Customization

### Import a Single CSV
```python
from utils.csv_importer import import_csv_corpus

# Import with custom prefix
import_csv_corpus(
    csv_path='path/to/your.csv',
    base_dir='data',
    prefix='custom'
)
```

### Access Imported Data
```python
import json

# Load metadata
with open('data/metadata.json', 'r', encoding='utf-8') as f:
    metadata = json.load(f)

# Filter by source
train_docs = {k: v for k, v in metadata.items() 
              if v['source'] == 'train.csv'}

# Filter by category
business_docs = {k: v for k, v in metadata.items() 
                 if v['category'] == 'business'}
```

## Corpus Statistics

After import, you can check statistics:

```python
from utils.csv_importer import get_category_stats

# Get category distribution
stats = get_category_stats(metadata)
for cat, count in sorted(stats.items()):
    print(f"{cat}: {count} documents")
```

## Integration with IR Modules

All IR modules automatically access the full corpus:

### Chapter 1: Foundations
```python
from core.ch01_foundations import Foundations

ir = Foundations('data/documents')
results = ir.boolean_search('your query')
```

### Chapter 5: Ranking
```python
from core.ch05_ranking import BM25

ranker = BM25('data/documents')
ranked = ranker.rank('your query')
```

## Data Structure

After import, your data directory looks like:

```
data/
├── documents/
│   ├── doc001.txt          # Original demo docs (if any)
│   ├── train0001.txt       # From train.csv
│   ├── train0002.txt
│   │   ...
│   ├── train5975.txt
│   ├── valid0001.txt       # From valid.csv
│   ├── valid0002.txt
│   │   ...
│   └── valid1495.txt
├── metadata.json           # All document metadata
├── stopwords.txt           # Nepali stopwords
├── web_graph.json          # Web link structure
└── qa_dataset.json         # QA pairs
```

## Metadata Schema

Each document in `metadata.json`:

```json
{
  "train0001": {
    "title": "Document heading from CSV",
    "author": "CSV Import - train",
    "date": "2025-01-17",
    "category": "business",
    "length": 145,
    "source": "train.csv"
  }
}
```

## Re-importing

To re-import (e.g., after updating CSVs):

1. **Backup existing data** (optional):
   ```bash
   copy data\metadata.json data\metadata.backup.json
   ```

2. **Remove old CSV imports**:
   ```bash
   del data\documents\train*.txt
   del data\documents\valid*.txt
   ```

3. **Re-run import**:
   ```bash
   python utils\csv_importer.py
   ```

## Troubleshooting

### "CSV file not found"
- Ensure `train.csv` and `valid.csv` are in the parent directory of `submission/`
- Or modify paths in `csv_importer.py` line 112-113

### "Memory error"
- For very large CSVs, process in chunks:
```python
import pandas as pd

chunksize = 1000
for chunk in pd.read_csv('large.csv', chunksize=chunksize):
    # Process chunk
    import_csv_corpus(chunk, base_dir, prefix)
```

### "Encoding errors"
- Ensure CSVs are UTF-8 encoded
- Use `encoding='utf-8'` in pandas:
```python
df = pd.read_csv('file.csv', encoding='utf-8')
```

## Best Practices

1. **Unique Prefixes**: Use different prefixes for different datasets
2. **Metadata**: Always update metadata.json when adding documents
3. **Validation**: Check document count after import
4. **Categories**: Use consistent category labels across datasets
5. **Backup**: Keep original CSVs as backup

## Performance Tips

- **Batch Processing**: Import large datasets in batches
- **Indexing**: Rebuild indices after bulk imports
- **Caching**: Clear any cached data after import

---

For more information, see:
- [csv_importer.py](file:///e:/Fulbutte/Desktop/information_retrieval/submission/utils/csv_importer.py) - Import implementation
- [CSV Import Verification](file:///C:/Users/fulbutte/.gemini/antigravity/brain/7a87e564-0da2-41db-b17f-0175db0925c2/csv_import_verification.md) - Import results and statistics
