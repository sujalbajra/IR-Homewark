
import os
import re
from pathlib import Path

def extract_sample_wordnet():
    # Paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    CORPUS_PATH = BASE_DIR / 'data' / 'nepali_corpus.txt'
    # Source IWN path (assuming it's a sibling of submission or known path)
    # The user environment has it at e:\Fulbutte\Desktop\information_retrieval\nepali_iwn
    SOURCE_IWN_DIR = BASE_DIR.parent / 'nepali_iwn' / 'data' / 'iwn_data'
    
    DEST_IWN_DIR = BASE_DIR / 'data' / 'iwn_data'
    DEST_SYNSETS_DIR = DEST_IWN_DIR / 'synsets'
    
    print(f"Reading corpus from {CORPUS_PATH}")
    vocab = set()
    with open(CORPUS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            for w in words:
                # Simple cleaning
                w = "".join(c for c in w if c.isalnum())
                if w:
                    vocab.add(w)
    
    print(f"Found {len(vocab)} unique words in corpus.")
    
    # Read Synsets
    synset_file = SOURCE_IWN_DIR / 'synsets' / 'all.nepali'
    if not synset_file.exists():
        print(f"Source synset file not found: {synset_file}")
        return

    print("Filtering synsets...")
    kept_synsets = []
    kept_ids = set()
    
    with open(synset_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                synset_id = parts[0]
                words = parts[1].split(',')
                # Check overlap
                if any(w in vocab for w in words):
                    kept_synsets.append(line)
                    kept_ids.add(synset_id)
    
    print(f"Kept {len(kept_synsets)} synsets relevant to corpus.")
    
    # Ensure dest dirs
    DEST_SYNSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Write filtered synsets
    dest_file = DEST_SYNSETS_DIR / 'all.nepali'
    with open(dest_file, 'w', encoding='utf-8') as f:
        f.writelines(kept_synsets)
        
    print(f"Saved to {dest_file}")

    # Copy minimal Ontology and Relations (Mocking or Full Copy?)
    # For now, let's copy ontology nodes/map if they exist, filtering might be too complex for now
    # Or just create empty files if the code handles missing files gracefully (it does check os.path.exists)
    
    # Copy Ontology (Nodes only?)
    # iwn.py checks for ontology/nodes and ontology/map
    
    DEST_ONTO_DIR = DEST_IWN_DIR / 'ontology'
    DEST_ONTO_DIR.mkdir(exist_ok=True)
    
    src_nodes = SOURCE_IWN_DIR / 'ontology' / 'nodes'
    if src_nodes.exists():
        # Just copy first 100 lines or all? Nodes file is usually small.
        # Let's copy all for now as filtered synsets might point relatively anywhere
        # Actually, let's just copy the file.
        import shutil
        shutil.copy(src_nodes, DEST_ONTO_DIR / 'nodes')
        shutil.copy(SOURCE_IWN_DIR / 'ontology' / 'map', DEST_ONTO_DIR / 'map')
        print("Copied ontology files.")

if __name__ == '__main__':
    extract_sample_wordnet()
