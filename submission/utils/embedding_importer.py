import os
import numpy as np
from tqdm import tqdm
import sys

# Add parent dir to path to import nepalikit/core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add nepalikit path specifically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nepalikit-main')))

from core.ch02_text_analysis import TextAnalysis

def import_embeddings(vec_path, docs_dir, output_path):
    print("Step 1: Building Vocabulary from Corpus...")
    vocab = set()
    
    # Initialize tokenizer with correct data dir (though not strictly needed for basic tokenize)
    # Using raw path to avoid config dependency
    analyzer = TextAnalysis("submission/data") 
    
    # Scan all documents
    files = [f for f in os.listdir(docs_dir) if f.endswith('.txt')]
    print(f"Scanning {len(files)} documents...")
    
    for filename in tqdm(files):
        with open(os.path.join(docs_dir, filename), 'r', encoding='utf-8') as f:
            text = f.read()
            # Use the robust tokenizer via analyze_text
            analysis = analyzer.analyze_text(text)
            tokens = analysis.get('tokens', [])
            vocab.update(tokens)
            
    print(f"Found {len(vocab)} unique tokens in corpus.")
    
    print("Step 2: Filtering Embeddings...")
    embeddings = {}
    found_count = 0
    
    with open(vec_path, 'r', encoding='utf-8', errors='ignore') as f:
        # Skip header if present (check if first line is metadata)
        first_line = f.readline().strip().split()
        if len(first_line) == 2:
            dims = int(first_line[1])
            print(f"Detected vector dimensions: {dims}")
        else:
            # No header, reset pointer
            f.seek(0)
            dims = len(first_line) - 1
            print(f"Detected vector dimensions (inferred): {dims}")
            
        # Stream file
        for line in tqdm(f, desc="Processing vectors"):
            parts = line.rstrip().split(' ')
            word = parts[0]
            
            if word in vocab:
                try:
                    vec = np.array(parts[1:], dtype=np.float32)
                    if len(vec) == dims:
                        embeddings[word] = vec
                        found_count += 1
                except ValueError:
                    continue
                    
    print(f"Matched {found_count} embeddings out of {len(vocab)} corpus tokens.")
    
    # Add special tokens
    if '<UNK>' not in embeddings:
        embeddings['<UNK>'] = np.zeros(dims, dtype=np.float32)
        
    print(f"Step 3: Saving to {output_path}...")
    np.savez_compressed(output_path, embeddings=embeddings)
    print("Done!")

if __name__ == "__main__":
    # Assuming running from submission/ directory
    VEC_FILE = "e:/Fulbutte/Desktop/information_retrieval/cc.ne.300.vec"
    DOCS_DIR = os.path.abspath("data/documents")
    OUTPUT_FILE = os.path.abspath("data/nepali_embeddings.npz")
    
    # Check if we are in root or submission
    if not os.path.exists("data/documents") and os.path.exists("submission/data/documents"):
        # We are likely in root
        DOCS_DIR = os.path.abspath("submission/data/documents")
        OUTPUT_FILE = os.path.abspath("submission/data/nepali_embeddings.npz")

    print(f"Vector File: {VEC_FILE}")
    print(f"Docs Dir: {DOCS_DIR}")
    print(f"Output File: {OUTPUT_FILE}")
    
    if not os.path.exists(VEC_FILE):
        print(f"Error: Vector file not found at {VEC_FILE}")
    elif not os.path.exists(DOCS_DIR):
        print(f"Error: Docs directory not found at {DOCS_DIR}")
    else:
        import_embeddings(VEC_FILE, DOCS_DIR, OUTPUT_FILE)
