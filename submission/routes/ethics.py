
from flask import Blueprint, render_template, current_app
from core.ethics.bias_detector import BiasDetector
import os

ethics_bp = Blueprint('ethics', __name__)

@ethics_bp.route('/ethics/bias')
def bias_analysis():
    docs = {}
    doc_dir = current_app.config['DOC_DIR']
    
    if os.path.exists(doc_dir):
        for f in os.listdir(doc_dir):
            if f.endswith('.txt'):
                with open(os.path.join(doc_dir, f), 'r', encoding='utf-8') as file:
                    docs[f] = file.read()
                    
    detector = BiasDetector()
    corpus_stats = detector.analyze_corpus(docs)
    
    # Detailed doc analysis
    doc_details = []
    for doc_id, text in docs.items():
        analysis = detector.analyze_text(text)
        analysis['doc_id'] = doc_id
        doc_details.append(analysis)
        
    return render_template('ethics/analysis.html', 
                          stats=corpus_stats, 
                          details=doc_details)
