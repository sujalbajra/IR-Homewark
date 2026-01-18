
import os
import math
import numpy as np
import json
import networkx as nx
from collections import Counter, defaultdict
from .ch02_text_analysis import TextAnalysis

class Ranking:
    def __init__(self, data_dir, doc_dir):
        self.doc_dir = doc_dir
        self.data_dir = data_dir
        self.analyzer = TextAnalysis(data_dir)
        self.documents = self._load_documents()
        self.N = len(self.documents)
        self.doc_lengths = {doc_id: len(text.split()) for doc_id, text in self.documents.items()}
        self.avg_dl = sum(self.doc_lengths.values()) / self.N if self.N > 0 else 0
        
        # Precompute Stats for TF-IDF/BM25
        self.df = defaultdict(int)
        self.tf = defaultdict(lambda: defaultdict(int))
        self._compute_stats()
        
    def _load_documents(self):
        docs = {}
        if os.path.exists(self.doc_dir):
            for filename in os.listdir(self.doc_dir):
                if filename.endswith('.txt'):
                    with open(os.path.join(self.doc_dir, filename), 'r', encoding='utf-8') as f:
                        docs[filename] = f.read()
        return docs

    def _compute_stats(self):
        for doc_id, text in self.documents.items():
            analysis = self.analyzer.analyze_text(text)
            terms = analysis['stemmed']
            term_counts = Counter(terms)
            
            for term, count in term_counts.items():
                self.df[term] += 1
                self.tf[doc_id][term] = count

    def compute_bm25(self, query, k1=1.5, b=0.75):
        query_terms = self.analyzer.analyze_text(query)['stemmed']
        scores = defaultdict(float)
        
        for term in query_terms:
            if term not in self.df:
                continue
                
            df = self.df[term]
            idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1)
            
            for doc_id in self.documents:
                tf = self.tf[doc_id].get(term, 0)
                dl = self.doc_lengths[doc_id]
                
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * (dl / self.avg_dl))
                
                scores[doc_id] += idf * (numerator / denominator)
                
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def compute_tfidf(self, query):
        query_terms = self.analyzer.analyze_text(query)['stemmed']
        scores = defaultdict(float)
        
        for term in query_terms:
            if term not in self.df:
                continue
            
            idf = math.log(self.N / (self.df[term] + 1))
            
            for doc_id in self.documents:
                tf = self.tf[doc_id].get(term, 0)
                # Log normalization for TF
                tf_norm = (1 + math.log(tf)) if tf > 0 else 0
                scores[doc_id] += tf_norm * idf
                
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def compute_bim(self, query):
        """Binary Independence Model (BIM) Ranking"""
        query_terms = self.analyzer.analyze_text(query)['stemmed']
        scores = defaultdict(float)
        
        for term in query_terms:
            if term not in self.df:
                continue
                
            # Weight is derived from probabilistic odds (smoothed)
            df = self.df[term]
            # RSV weight: log( (N - df + 0.5) / (df + 0.5) )
            # This represents the log-odds ratio of term appearing in relevant vs non-relevant docs, assuming R=0
            weight = math.log((self.N - df + 0.5) / (df + 0.5))
            
            for doc_id in self.documents:
                # Binary: checks presence only, ignores frequency
                if self.tf[doc_id].get(term, 0) > 0:
                    scores[doc_id] += weight
                    
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def build_synthetic_graph(self):
        """
        Builds a synthetic link graph based on content content overlap.
        Concept: 
        1. Identify a 'Topic Word' for each document from its first line (title).
        2. If Doc A contains Doc B's Topic Word, we assume a citation A -> B.
        """
        doc_signatures = {}
        
        # Step 1: Extract signatures (Topic Words)
        for doc_id, text in self.documents.items():
            # Get first line or first 10 tokens
            first_line = text.split('\n')[0]
            analysis = self.analyzer.analyze_text(first_line)
            tokens = analysis['tokens']
            
            # Find first non-stopword, non-numeric token as "Title Topic"
            signature = None
            for t in tokens:
                if t.lower() not in self.analyzer.stopwords and t.isalpha() and len(t) > 3:
                    signature = t
                    break
            
            if signature:
                doc_signatures[doc_id] = signature

        # Step 2: Build Edges
        nodes = [{'id': doc_id, 'label': sig} for doc_id, sig in doc_signatures.items()]
        edges = []
        
        for source_id, text in self.documents.items():
            source_tokens = set(self.analyzer.analyze_text(text)['tokens'])
            
            for target_id, signature in doc_signatures.items():
                if source_id == target_id: continue
                
                # Check if source contains target's signature
                if signature in source_tokens:
                    edges.append({'source': source_id, 'target': target_id})
        
        graph_data = {'nodes': nodes, 'edges': edges}
        
        # Save to file
        graph_path = os.path.join(self.data_dir, 'web_graph.json')
        with open(graph_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
            
        return graph_data

    def compute_pagerank(self):
        graph_path = os.path.join(self.data_dir, 'web_graph.json')
        
        # Auto-build if missing
        if not os.path.exists(graph_path):
            self.build_synthetic_graph()
            
        if not os.path.exists(graph_path):
             return []

        with open(graph_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        G = nx.DiGraph()
        # Add all documents as nodes to ensure isolated ones are included
        for doc_id in self.documents:
            G.add_node(doc_id)
            
        for edge in data['edges']:
            G.add_edge(edge['source'], edge['target'])
            
        try:
            pr = nx.pagerank(G, alpha=0.85)
            # Add HITS
            try:
                hubs, authorities = nx.hits(G, max_iter=100, normalized=True)
            except nx.PowerIterationFailedConvergence:
                hubs, authorities = {}, {}
            
            combined = []
            for node in G.nodes():
                combined.append({
                    'node': node,
                    'pagerank': pr.get(node, 0),
                    'authority': authorities.get(node, 0),
                    'hub': hubs.get(node, 0)
                })
            return sorted(combined, key=lambda x: x['pagerank'], reverse=True)
        except Exception as e:
            print(f"Graph Error: {e}")
            return []
