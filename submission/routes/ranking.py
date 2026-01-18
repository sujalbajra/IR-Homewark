from flask import Blueprint, render_template, request, current_app
from core.ch05_ranking import Ranking
from extensions import app_globals
import os

ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route('/ranking/compare', methods=['GET', 'POST'])
def ranking_compare():
    from core.ch21_word_analysis import WordAnalyzer
    from core.query_processor import QueryProcessor
    
    # Ensure dependencies are initialized
    if app_globals.ranker is None:
        app_globals.ranker = Ranking(current_app.config['DATA_DIR'], current_app.config['DOC_DIR'])
        
    if app_globals.word_analyzer is None:
        app_globals.word_analyzer = WordAnalyzer(current_app.config['DATA_DIR'], current_app.config['DOC_DIR'])
        
    query_processor = QueryProcessor(app_globals.word_analyzer)
    
    results_bm25 = []
    results_tfidf = []
    doc_previews = {}
    query = None
    query_analysis = None
    k1, b = 1.5, 0.75
    
    if request.method == 'POST':
        query = request.form.get('query')
        k1 = float(request.form.get('k1', 1.5))
        b = float(request.form.get('b', 0.75))
        top_k = int(request.form.get('top_k', 10))
        
        # Analyze Query
        query_analysis = query_processor.process_query(query)
        
        results_bm25 = app_globals.ranker.compute_bm25(query, k1, b)[:top_k]
        results_tfidf = app_globals.ranker.compute_tfidf(query)[:top_k]
        results_bim = app_globals.ranker.compute_bim(query)[:top_k]
        
        # Load previews for all retrieved docs
        all_docs = set([doc for doc, _ in results_bm25] + [doc for doc, _ in results_tfidf] + [doc for doc, _ in results_bim])
        for doc_id in all_docs:
            try:
                with open(os.path.join(current_app.config['DOC_DIR'], doc_id), 'r', encoding='utf-8') as f:
                    content = f.read()
                    doc_previews[doc_id] = content[:150] + ('...' if len(content) > 150 else '')
            except:
                doc_previews[doc_id] = "Preview not available"
    
    return render_template('ranking/compare.html', 
                          results_bm25=results_bm25, 
                          results_tfidf=results_tfidf,
                          results_bim=results_bim,
                          doc_previews=doc_previews,
                          query=query, k1=k1, b=b,
                          query_analysis=query_analysis,
                          top_k=request.form.get('top_k', 10))

@ranking_bp.route('/ranking/pagerank')
def ranking_pagerank():
    if app_globals.ranker is None:
        app_globals.ranker = Ranking(current_app.config['DATA_DIR'], current_app.config['DOC_DIR'])
    graph_data = app_globals.ranker.compute_pagerank()
    return render_template('ranking/pagerank.html', graph_data=graph_data)
