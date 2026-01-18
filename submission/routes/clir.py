
from flask import Blueprint, render_template, request, current_app
from core.translation.dictionary_translator import DictionaryTranslator
from core.ch05_ranking import Ranking
from extensions import app_globals
import os

clir_bp = Blueprint('clir', __name__)

@clir_bp.route('/clir/search', methods=['GET', 'POST'])
def search():
    query_en = None
    query_ne = None
    results = []
    
    if request.method == 'POST':
        query_en = request.form.get('query')
        
        # 1. Translate
        translator = DictionaryTranslator()
        query_ne = translator.translate_query(query_en)
        
        # 2. Search (using BM25 on translated query)
        if app_globals.ranker is None:
            app_globals.ranker = Ranking(current_app.config['DATA_DIR'], current_app.config['DOC_DIR'])
            
        results = app_globals.ranker.compute_bm25(query_ne)[:10]
        
    return render_template('clir/search.html', 
                          query_en=query_en, 
                          query_ne=query_ne, 
                          results=results)
