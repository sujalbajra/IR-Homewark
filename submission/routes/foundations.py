from flask import Blueprint, render_template, request, current_app
import os
from core.ch01_foundations import Foundations

foundations_bp = Blueprint('foundations', __name__)

@foundations_bp.route('/foundations/boolean', methods=['GET', 'POST'])
def boolean_search():
    results = None
    doc_previews = {}
    if request.method == 'POST':
        query = request.form.get('query')
        op = request.form.get('operation')
        foundation = Foundations(current_app.config['DOC_DIR'])
        results = foundation.boolean_search(query, op)
        
        # Load previews for tooltip
        for doc_id in results:
            try:
                with open(os.path.join(current_app.config['DOC_DIR'], doc_id), 'r', encoding='utf-8') as f:
                    content = f.read()
                    doc_previews[doc_id] = content[:150] + ('...' if len(content) > 150 else '')
            except:
                doc_previews[doc_id] = "Preview not available"
                
    return render_template('foundations/boolean.html', results=results, doc_previews=doc_previews)

@foundations_bp.route('/foundations/vsm', methods=['GET', 'POST'])
def vector_space_model():
    results = None
    doc_previews = {}
    if request.method == 'POST':
        query = request.form.get('query')
        foundation = Foundations(current_app.config['DOC_DIR'])
        results = foundation.compute_cosine_similarity(query)
        
        # Load previews
        for doc_id, score in results:
            try:
                with open(os.path.join(current_app.config['DOC_DIR'], doc_id), 'r', encoding='utf-8') as f:
                    content = f.read()
                    doc_previews[doc_id] = content[:150] + ('...' if len(content) > 150 else '')
            except:
                doc_previews[doc_id] = "Preview not available"
                
    return render_template('foundations/vsm.html', results=results, doc_previews=doc_previews)
