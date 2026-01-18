from flask import Blueprint, render_template, request, current_app
from core.ch04_query_proc import QueryProcessing
from core.ch03_indexing import Indexing
from extensions import app_globals

query_proc_bp = Blueprint('query_proc', __name__)

@query_proc_bp.route('/query/wildcard', methods=['GET', 'POST'])
def query_wildcard():
    results = None
    pattern = None
    if request.method == 'POST':
        pattern = request.form.get('pattern')
        
        # Validate pattern
        if pattern and pattern.strip():
            if app_globals.indexer is None:
                app_globals.indexer = Indexing(current_app.config['DATA_DIR'], current_app.config['DOC_DIR'])
                app_globals.indexer.build_indexes()
            
            qp = QueryProcessing(current_app.config['DATA_DIR'])
            vocab = list(app_globals.indexer.inverted_index.keys())
            results = qp.match_wildcard(pattern, vocab)
        else:
             results = []
    return render_template('query/wildcard.html', results=results, pattern=pattern)

@query_proc_bp.route('/query/spellcheck', methods=['GET', 'POST'])
def query_spellcheck():
    suggestions = None
    word = None
    if request.method == 'POST':
        word = request.form.get('word')
        
        if app_globals.indexer is None:
            app_globals.indexer = Indexing(current_app.config['DATA_DIR'], current_app.config['DOC_DIR'])
            app_globals.indexer.build_indexes()
        
        qp = QueryProcessing(current_app.config['DATA_DIR'])
        # Use simple vocabulary from inverted index
        vocab = list(app_globals.indexer.inverted_index.keys()) 
        # Add some common English/Nepali words if vocab is small
        if len(vocab) < 100:
            vocab.extend(['nepal', 'kathmandu', 'search', 'engine', 'computer', 'science'])
            
        suggestions = qp.spell_suggest(word, vocab)
        
    return render_template('query/spellcheck.html', suggestions=suggestions, word=word)
