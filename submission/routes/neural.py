from flask import Blueprint, render_template, request, current_app
from core.ch06_neural import NeuralIR
import os

neural_bp = Blueprint('neural', __name__)

@neural_bp.route('/neural/search', methods=['GET', 'POST'])
def neural_search():
    results = None
    rag_answer = None
    context_preview = None
    query = None
    
    if request.method == 'POST':
        query = request.form.get('query')
        use_rerank = request.form.get('rerank') == 'on'
        
        docs = {}
        doc_dir = current_app.config['DOC_DIR']
        if os.path.exists(doc_dir):
            for f in os.listdir(doc_dir)[:20]:
                if f.endswith('.txt'):
                    with open(os.path.join(doc_dir, f), 'r', encoding='utf-8') as file:
                        docs[f] = file.read()
        
        neural = NeuralIR(current_app.config['DATA_DIR'])
        
        if use_rerank:
            # Hybrid: BM25 first, then Neural Rerank
            from extensions import app_globals
            from core.ch05_ranking import Ranking
            
            if app_globals.ranker is None:
                app_globals.ranker = Ranking(current_app.config['DATA_DIR'], current_app.config['DOC_DIR'])
            
            # 1. Get BM25 results (Initial Retrieval)
            bm25_results = app_globals.ranker.compute_bm25(query)[:20] # Top 20 candidate generation
            
            # 2. Neural Re-ranking
            results = neural.neural_rerank(query, bm25_results, docs)
            
        else:
            # Pure Dense Retrieval
            results = neural.dense_retrieval(query, docs)
        
        if results:
            top_docs = results[:2]
            rag_answer = neural.mock_rag_generation(query, top_docs)
            if top_docs[0][0] in docs:
                context_preview = (docs[top_docs[0][0]][:100] + "...")
            else:
                context_preview = "Preview unavailable"
    
    return render_template('neural/search.html', 
                          results=results, 
                          rag_answer=rag_answer,
                          query=query,
                          context_preview=context_preview)
