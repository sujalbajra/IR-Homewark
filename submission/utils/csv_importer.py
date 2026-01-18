
import os
import json
import pandas as pd
from pathlib import Path


def ensure_dir(path):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)


def import_csv_corpus(csv_path, base_dir, prefix='csv'):
    """
    Import CSV data into the document corpus.
    
    Args:
        csv_path: Path to the CSV file
        base_dir: Base data directory
        prefix: Prefix for document IDs (e.g., 'train' or 'valid')
    
    Returns:
        List of document IDs that were imported
    """
    # Read CSV file
    df = pd.read_csv(csv_path)
    
    # Create documents directory
    docs_dir = os.path.join(base_dir, 'documents')
    ensure_dir(docs_dir)
    
    # Load existing metadata if available
    metadata_path = os.path.join(base_dir, 'metadata.json')
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    else:
        metadata = {}
    
    imported_ids = []
    
    print(f"Importing {len(df)} documents from {csv_path}...")
    
    for idx, row in df.iterrows():
        # Create unique document ID
        doc_id = f"{prefix}{idx+1:04d}"
        
        # Combine heading and paragraph as document content
        heading = str(row['headings']) if pd.notna(row['headings']) else ""
        para = str(row['paras']) if pd.notna(row['paras']) else ""
        
        # Create full content
        if heading and para:
            content = f"{heading}\n\n{para}"
        else:
            content = heading or para
        
        # Save document as .txt file
        doc_path = os.path.join(docs_dir, f"{doc_id}.txt")
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Add to metadata
        metadata[doc_id] = {
            "title": heading if heading else f"Document {doc_id}",
            "author": f"CSV Import - {prefix}",
            "date": "2025-01-17",
            "category": str(row['label']) if pd.notna(row['label']) else "unknown",
            "length": len(content.split()),
            "source": os.path.basename(csv_path)
        }
        
        imported_ids.append(doc_id)
    
    # Save updated metadata
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Imported {len(imported_ids)} documents with prefix '{prefix}'")
    return imported_ids


def get_category_stats(metadata):
    """Get statistics about imported categories"""
    categories = {}
    for doc_id, meta in metadata.items():
        cat = meta.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    return categories


def main():
    """Main import function"""
    # Determine base directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    submission_dir = os.path.dirname(script_dir)
    base_dir = os.path.join(submission_dir, 'data')
    
    # Paths to CSV files (one level above submission)
    parent_dir = os.path.dirname(submission_dir)
    train_csv = os.path.join(parent_dir, 'train.csv')
    valid_csv = os.path.join(parent_dir, 'valid.csv')
    
    ensure_dir(base_dir)
    
    # Import both CSV files
    all_imported = []
    
    if os.path.exists(train_csv):
        train_ids = import_csv_corpus(train_csv, base_dir, prefix='train')
        all_imported.extend(train_ids)
    else:
        print(f"Warning: {train_csv} not found")
    
    if os.path.exists(valid_csv):
        valid_ids = import_csv_corpus(valid_csv, base_dir, prefix='valid')
        all_imported.extend(valid_ids)
    else:
        print(f"Warning: {valid_csv} not found")
    
    # Load final metadata and show stats
    metadata_path = os.path.join(base_dir, 'metadata.json')
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    print(f"\n{'='*60}")
    print(f"IMPORT SUMMARY")
    print(f"{'='*60}")
    print(f"Total documents in corpus: {len(metadata)}")
    print(f"Newly imported: {len(all_imported)}")
    print(f"\nCategory Distribution:")
    
    stats = get_category_stats(metadata)
    for cat, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:15s}: {count:4d} documents")
    
    print(f"\nData location: {base_dir}")
    print(f"{'='*60}")
    

if __name__ == "__main__":
    main()
