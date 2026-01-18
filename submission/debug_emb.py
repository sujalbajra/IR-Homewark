import numpy as np
import os

path = "submission/data/nepali_embeddings.npz"
if not os.path.exists(path):
    print(f"File not found: {path}")
    path = "data/nepali_embeddings.npz"

if os.path.exists(path):
    print(f"Loading {path}...")
    try:
        data = np.load(path, allow_pickle=True)
        print(f"Keys: {list(data.keys())}")
        if 'embeddings' in data:
            emb = data['embeddings']
            print(f"Type: {type(emb)}")
            print(f"Shape: {emb.shape}")
            
            if emb.shape == ():
                print("Detected 0-d array (wrapped dict). Needs .item()")
                real_emb = emb.item()
                print(f"Real dict type: {type(real_emb)}")
                print(f"Vocab size: {len(real_emb)}")
            else:
                print("Detected normal array/dict")
        else:
            print("'embeddings' key missing")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("File still not found.")
