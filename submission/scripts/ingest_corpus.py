
import os

CORPUS_FILE = r'e:\Fulbutte\Desktop\information_retrieval\submission\data\nepali_corpus.txt'
OUTPUT_DIR = r'e:\Fulbutte\Desktop\information_retrieval\submission\data\documents'

def ingest_corpus():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Reading {CORPUS_FILE}...")
    try:
        with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        print(f"Found {len(lines)} lines. Creating documents...")
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Create file doc_001.txt, etc.
            doc_name = f"doc_{i+1:03d}.txt"
            doc_path = os.path.join(OUTPUT_DIR, doc_name)
            
            with open(doc_path, 'w', encoding='utf-8') as out:
                out.write(line)
                
        print(f"Successfully created {len(lines)} documents in {OUTPUT_DIR}")
        
    except FileNotFoundError:
        print("Corpus file not found!")

if __name__ == "__main__":
    ingest_corpus()
