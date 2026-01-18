from flask import Blueprint, render_template, request, current_app
from core.ch08_web_search import WebSearch

web_search_bp = Blueprint('web_search', __name__)

@web_search_bp.route('/web/duplicates', methods=['GET', 'POST'])
def web_duplicates():
    results = None
    text_a = None
    text_b = None
    
    if request.method == 'POST':
        text_a = request.form.get('text_a')
        text_b = request.form.get('text_b')
        searcher = WebSearch(current_app.config['DATA_DIR'])
        hash_a = searcher.compute_simhash(text_a)
        hash_b = searcher.compute_simhash(text_b)
        dist = searcher.hamming_distance(hash_a, hash_b)
        results = {'hash_a': hash_a, 'hash_b': hash_b, 'distance': dist}
    
    return render_template('web/duplicates.html', results=results, text_a=text_a, text_b=text_b)

@web_search_bp.route('/web/spam', methods=['GET', 'POST'])
def web_spam():
    score = None
    reasons = None
    content = None
    
    if request.method == 'POST':
        content = request.form.get('content')
        searcher = WebSearch(current_app.config['DATA_DIR'])
        score, reasons = searcher.detect_spam(content)
    
    return render_template('web/spam.html', score=score, reasons=reasons, content=content)
