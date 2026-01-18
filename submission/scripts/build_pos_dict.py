
import csv
import json
import os
from collections import Counter, defaultdict

INPUT_FILE = r'e:\Fulbutte\Desktop\information_retrieval\pos_tags_with_suffix.csv'
OUTPUT_FILE = r'e:\Fulbutte\Desktop\information_retrieval\submission\data\id_pos_dict.json'

def build_pos_dict():
    print(f"Reading {INPUT_FILE}...")
    
    # Word -> Counter of POS tags
    word_pos_counts = defaultdict(Counter)
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for i, row in enumerate(reader):
                word = row['words'].strip()
                pos = row['pos'].strip()
                
                if word and pos:
                    word_pos_counts[word][pos] += 1
                    
                if i % 100000 == 0:
                    print(f"Processed {i} lines...")
                    if i > 1000000: # Limit to 1M lines for speed in this demo
                         break 
                         
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print("Building final dictionary...")
    final_dict = {}
    for word, counts in word_pos_counts.items():
        # Get most frequent POS tag for the word
        most_common_pos = counts.most_common(1)[0][0]
        final_dict[word] = most_common_pos
        
    print(f"Saving {len(final_dict)} words to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)
        
    print("Done!")

if __name__ == "__main__":
    build_pos_dict()
