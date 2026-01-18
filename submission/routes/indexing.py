from flask import Blueprint, render_template, request, current_app
from core.ch03_indexing import Indexing
from extensions import app_globals

indexing_bp = Blueprint('indexing', __name__)

@indexing_bp.route('/indexing', methods=['GET', 'POST'])
def indexing_demo():
    if app_globals.indexer is None:
        app_globals.indexer = Indexing(current_app.config['DATA_DIR'], current_app.config['DOC_DIR'])
        stats = app_globals.indexer.build_indexes()
    else:
        stats = {
            'doc_count': len(app_globals.indexer.positional_index),
            'vocab_size': len(app_globals.indexer.inverted_index),
            'total_tokens': "N/A (Cached)" 
        }

    term_data = None
    if request.method == 'POST':
        term = request.form.get('term')
        if term:
            postings = app_globals.indexer.get_posting_list(term)
            positional = app_globals.indexer.get_positional_postings(term)
            sample_doc_id = abs(hash(term)) % 10000 
            compressed = app_globals.indexer.variable_byte_encode(sample_doc_id)
            term_data = {
                'term': term,
                'postings': postings,
                'positional': positional,
                'sample_doc_id': sample_doc_id,
                'compressed_bytes': compressed
            }
    return render_template('indexing/view.html', stats=stats, term_data=term_data)
