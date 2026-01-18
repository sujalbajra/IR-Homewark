"""
Update web graph for PageRank/HITS to include all corpus documents.
This script regenerates the web_graph.json file with the full corpus.
"""

import os
import json
import random
import networkx as nx


def get_all_document_ids(doc_dir):
    """Get all document IDs from the documents directory."""
    doc_ids = []
    if os.path.exists(doc_dir):
        for filename in os.listdir(doc_dir):
            if filename.endswith('.txt'):
                # Use filename without extension as doc ID
                doc_id = filename[:-4]  # Remove .txt
                doc_ids.append(doc_id)
    return sorted(doc_ids)


def generate_web_graph(base_dir, doc_ids, edge_probability=0.02):
    """
    Generate a web graph for PageRank/HITS algorithms.
    
    Args:
        base_dir: Directory to save the graph
        doc_ids: List of document IDs to include
        edge_probability: Probability of creating an edge between documents
                         Lower values for large corpora to avoid excessive edges
    """
    print(f"Generating web graph for {len(doc_ids)} documents...")
    
    # For large corpora, use a scale-free graph model
    # This mimics real web link structures (power law distribution)
    if len(doc_ids) > 100:
        # Barabási-Albert model: preferential attachment
        # m = number of edges to attach from new node (keep it small for efficiency)
        m = min(3, len(doc_ids) // 100)
        G = nx.barabasi_albert_graph(len(doc_ids), m, seed=42)
    else:
        # For smaller graphs, use Erdős-Rényi random graph
        G = nx.erdos_renyi_graph(len(doc_ids), edge_probability, seed=42, directed=True)
    
    graph_data = {"nodes": [], "edges": []}
    
    # Map graph indices to doc IDs
    node_map = {i: doc_id for i, doc_id in enumerate(doc_ids)}
    
    # Add all nodes
    for idx, doc_id in node_map.items():
        graph_data["nodes"].append({"id": doc_id})
    
    # Add edges
    edge_count = 0
    for u, v in G.edges():
        if u in node_map and v in node_map and u != v:
            graph_data["edges"].append({
                "source": node_map[u],
                "target": node_map[v]
            })
            edge_count += 1
    
    # Save graph
    graph_path = os.path.join(base_dir, 'web_graph.json')
    with open(graph_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2)
    
    print(f"✓ Generated web graph:")
    print(f"  - Nodes: {len(graph_data['nodes'])}")
    print(f"  - Edges: {len(graph_data['edges'])}")
    print(f"  - Avg degree: {edge_count / len(doc_ids):.2f}")
    print(f"  - Saved to: {graph_path}")
    
    return graph_path


def main():
    """Main function to regenerate web graph."""
    # Determine paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    submission_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(submission_dir, 'data')
    doc_dir = os.path.join(data_dir, 'documents')
    
    # Get all document IDs
    doc_ids = get_all_document_ids(doc_dir)
    
    if not doc_ids:
        print("Error: No documents found in", doc_dir)
        return
    
    print(f"Found {len(doc_ids)} documents in corpus")
    print(f"Sample IDs: {doc_ids[:5]}...")
    print()
    
    # Generate graph
    generate_web_graph(data_dir, doc_ids, edge_probability=0.02)
    
    print()
    print("="*60)
    print("Web graph updated successfully!")
    print("PageRank and HITS algorithms will now use the full corpus.")
    print("="*60)


if __name__ == "__main__":
    main()
