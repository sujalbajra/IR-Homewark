# Information Retrieval System for Nepali Language

A comprehensive educational implementation of Information Retrieval concepts and algorithms for Nepali language using **vanilla Python** (no external NLP libraries).

---

## 📚 Overview

This project provides a complete learning path through Information Retrieval, from basic concepts to advanced techniques, all implemented in Nepali language context. Perfect for students and researchers interested in IR fundamentals.

### Inspiration

Based on the awesome [awesome-information-retrieval](https://github.com/harpribot/awesome-information-retrieval) repository and university IR courses, covering foundational concepts from:
- Boolean Retrieval Models
- Inverted Indices
- Vector Space Models
- TF-IDF & BM25 Ranking
- Advanced Evaluation Metrics (NDCG, MAP)
- Spell Checking & Autocomplete
- Query Expansion

---

## 🗂️ Project Structure

```
information_retrieval/
├── data/                      # Document collection & resources
│   ├── doc01.txt - doc10.txt # 10 Nepali documents (various topics)
│   ├── nepali_stopwords.csv  # Stopword list
│   └── nepali_stemming.csv   # Word→stem mapping
│
└── notebooks/                 # Jupyter notebooks (educational)
    ├── 01_data_preparation.ipynb
    ├── 02_text_preprocessing.ipynb
    ├── 03_boolean_retrieval.ipynb
    ├── 04_inverted_index.ipynb
    ├── 04_01_positional_index.ipynb (Proximity Search)
    ├── 05_vector_space_model.ipynb
    ├── 06_tf_idf_ranking.ipynb
    ├── 06_02_bm25_ranking.ipynb (Probabilistic Ranking)
    ├── 07_language_modeling.ipynb (Smoothing Implemented)
    ├── 08_evaluation_metrics.ipynb (NDCG, MAP, MRR Added)
    ├── 09_query_expansion.ipynb (Co-occurrence Added)
    ├── 09_01_rocchio.ipynb (Relevance Feedback)
    ├── 10_cross_lingual_ir.ipynb (Conceptual)
    ├── 10_01_naive_bayes.ipynb (Classification)
    ├── 11_spell_checking.ipynb (Edit Distance, N-Grams)
    └── 12_autocomplete.ipynb (Trie-based Suggestions)
```

---

## 📖 Notebook Contents

### 1. **Data Preparation** (`01_data_preparation.ipynb`)
- Loading document collections
- Exploratory data analysis
- Document statistics

### 2. **Text Preprocessing** (`02_text_preprocessing.ipynb`)
- **Tokenization**: Breaking text into words
- **Stopword Removal**: Filtering common words
- **Stemming**: Reducing words to root forms (using CSV mapping)

### 3. **Boolean Retrieval** (`03_boolean_retrieval.ipynb`)
- Document-term matrix construction
- Boolean operators (AND, OR, NOT)
- Set-based query processing

### 4. **Inverted Index & Positional Index** (`04_inverted_index.ipynb`, `04_01_positional_index.ipynb`)
- Building efficient inverted indices
- Posting lists structure
- Phrase queries and proximity search

### 5. **Vector Space Model** (`05_vector_space_model.ipynb`)
- Document vectors (term frequency)
- Cosine similarity computation
- Ranked retrieval

### 6. **Ranking Algorithms** (`06_tf_idf_ranking.ipynb`, `06_02_bm25_ranking.ipynb`)
- **TF-IDF**: Term Frequency & Inverse Document Frequency weighting
- **BM25**: State-of-the-art probabilistic ranking with length normalization and saturation

### 7. **Language Modeling** (`07_language_modeling.ipynb`)
- Unigram Language Models
- **Smoothing**: Jelinek-Mercer and Dirichlet Prior smoothing techniques
- Query likelihood ranking

### 8. **Evaluation Metrics** (`08_evaluation_metrics.ipynb`)
- Precision & Recall, F1-Score
- Mean Average Precision (**MAP**)
- Mean Reciprocal Rank (**MRR**)
- Normalized Discounted Cumulative Gain (**NDCG**)

### 9. **Query Processing** (`09_query_expansion.ipynb`, `09_01_rocchio.ipynb`)
- **Query Expansion**: Thesaurus and Co-occurrence based
- **Relevance Feedback**: Rocchio's algorithm implementation
- **Pseudo-Relevance Feedback**: Automatic expansion from top docs

### 10. **User Experience** (`11_spell_checking.ipynb`, `12_autocomplete.ipynb`)
- **Spell Checker**: Minimum Edit Distance (Levenshtein) & N-gram overlap
- **Autocomplete**: Trie data structure for fast prefix suggestions

### 11. **Classification** (`10_01_naive_bayes.ipynb`)
- Naive Bayes text classifier for document categorization

---

## 🚀 Getting Started

### Prerequisites

**Only vanilla Python required!**
- Python 3.7+
- Jupyter Notebook or JupyterLab
- Standard library only: `pathlib`, `collections`, `math`, `re`

No external NLP libraries needed (NLTK, spaCy, etc.)

### Installation

1. **Clone or download this project**
```bash
cd information_retrieval
```

2. **Verify structure**
```bash
# Should see:
# - data/ folder with 10 .txt files and 2 .csv files
# - notebooks/ folder with 16+ .ipynb files
```

3. **Start Jupyter**
```bash
jupyter notebook
```

4. **Open notebooks in order** (01 → 02 → ... → 12)

---

## 📅 Roadmap & Future Work

We are actively expanding this repository to cover more advanced topics:

### Upcoming Notebooks:
- [ ] **Topic Modeling** (`13_topic_modeling.ipynb`): Latent Dirichlet Allocation (LDA)
- [ ] **PageRank** (`14_pagerank.ipynb`): Link analysis and graph ranking
- [ ] **Web Crawling** (`15_web_crawling.ipynb`): Conceptual crawler design
- [ ] **Indexing Strategies** (`16_indexing_strategies.ipynb`): BSBI/SPIMI (simulated)
- [ ] **Embeddings & ANN** (`17_embeddings_and_ann.ipynb`): Vector embeddings and approximate nearest neighbors
- [ ] **Multimedia IR** (`18_multimedia_ir_concepts.ipynb`): Audio/Image search concepts

---

## 🔧 Vanilla Python Approach

### Why No External Libraries?

- ✅ **Educational clarity**: See how algorithms actually work
- ✅ **Easy to understand**: No black boxes
- ✅ **No installation issues**: Works everywhere
- ✅ **Concept focus**: Learn IR, not library APIs

### What We Use Instead:

| Need | Vanilla Python Solution |
|------|------------------------|
| **Stemming** | CSV mapping file (`nepali_stemming.csv`) |
| **Stopwords** | CSV list (`nepali_stopwords.csv`) |
| **Tokenization** | String splitting + unicode filtering |
| **Vectors** | Python lists |
| **Similarity** | Manual dot product & magnitude |
| **Indexing** | Python dictionaries & sets |
| **Tries/Graphs** | Custom Python classes |

---

## 📄 License

This is an educational project. Feel free to use for learning and teaching purposes.

Inspired by [awesome-information-retrieval](https://github.com/harpribot/awesome-information-retrieval) (CC0-1.0 License).

---

## 🙏 Acknowledgments

- **awesome-information-retrieval** repository by harpribot
- Manning, Raghavan & Schütze: *Introduction to Information Retrieval*
- Nepali language community

---

## 📬 Questions & Feedback

This project is designed for **educational purposes**. Experiment, learn, and build upon it!

**Happy Learning! 🎓🔍**
