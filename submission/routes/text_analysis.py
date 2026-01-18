from flask import Blueprint, render_template, request, current_app
from core.ch02_text_analysis import TextAnalysis

text_analysis_bp = Blueprint('text_analysis', __name__)

@text_analysis_bp.route('/text_analysis', methods=['GET', 'POST'])
def text_analysis_pipeline():
    results = None
    input_text = None
    if request.method == 'POST':
        input_text = request.form.get('text')
        analyzer = TextAnalysis(current_app.config['DATA_DIR'])
        results = analyzer.analyze_text(input_text)
    return render_template('text_analysis/pipeline.html', results=results, input_text=input_text)
