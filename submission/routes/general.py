from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
import os
from extensions import app_globals
from core.ch21_word_analysis import WordAnalyzer

general_bp = Blueprint('general', __name__)

@general_bp.route('/')
def index():
    """Dashboard showing system stats."""
    try:
        doc_count = len([n for n in os.listdir(current_app.config['DOC_DIR']) if n.endswith('.txt')])
    except FileNotFoundError:
        doc_count = 0
    return render_template('index.html', doc_count=doc_count)

@general_bp.route('/documents', methods=['GET', 'POST'])
def documents():
    """Document management."""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.txt'):
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
            flash(f'Uploaded {file.filename} successfully!')
            return redirect(url_for('general.documents'))
            
            return redirect(url_for('general.documents'))
            
    files = []
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Grid of 3x3
    
    if os.path.exists(current_app.config['DOC_DIR']):
        all_files = sorted([f for f in os.listdir(current_app.config['DOC_DIR']) if f.endswith('.txt')])
        total_files = len(all_files)
        total_pages = (total_files + per_page - 1) // per_page
        
        # Validation
        if page < 1: page = 1
        if page > total_pages and total_pages > 0: page = total_pages
        
        start = (page - 1) * per_page
        end = start + per_page
        files = all_files[start:end]
    else:
        total_pages = 0
        total_files = 0
        
    return render_template('upload.html', 
                         files=files, 
                         page=page, 
                         total_pages=total_pages,
                         total_files=total_files)

@general_bp.route('/documents/<filename>')
def view_document(filename):
    """View specific document content."""
    try:
        file_path = os.path.join(current_app.config['DOC_DIR'], filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Initialize analyzer if needed
        if 'word_analyzer' not in app_globals.__dict__ or app_globals.word_analyzer is None:
            app_globals.word_analyzer = WordAnalyzer(current_app.config['DATA_DIR'], current_app.config['DOC_DIR'])
            
        # Pagination Logic for Content
        page = request.args.get('p', 1, type=int)
        per_page = 15 # paragraphs per page
        
        paragraphs = [p for p in content.split('\n') if p.strip()]
        total_content_pages = (len(paragraphs) + per_page - 1) // per_page
        
        if page < 1: page = 1
        if page > total_content_pages and total_content_pages > 0: page = total_content_pages
        
        start = (page - 1) * per_page
        end = start + per_page
        current_paragraphs = paragraphs[start:end]
        
        # Annotate only the current page content
        annotated_html_parts = []
        for p_text in current_paragraphs:
            annotated_html_parts.append(app_globals.word_analyzer.annotate_document(p_text))
            
        final_annotated_content = '<p>' + '</p><p>'.join(annotated_html_parts) + '</p>'
        
        if not current_paragraphs: # Handle empty doc
            final_annotated_content = "<em>(Empty Page)</em>"
        
        # Calculate Next/Prev Document
        files = sorted([f for f in os.listdir(current_app.config['DOC_DIR']) if f.endswith('.txt')])
        try:
            curr_idx = files.index(filename)
            prev_file = files[curr_idx - 1] if curr_idx > 0 else None
            next_file = files[curr_idx + 1] if curr_idx < len(files) - 1 else None
        except ValueError:
            prev_file = None
            next_file = None
        
        return render_template('view_document.html', 
                             filename=filename, 
                             annotated_content=final_annotated_content,
                             prev_file=prev_file,
                             next_file=next_file,
                             current_page=page,
                             total_pages=total_content_pages)
    except FileNotFoundError:
        flash(f'Document {filename} not found.')
        return redirect(url_for('general.documents'))

@general_bp.route('/documents/delete/<filename>', methods=['POST'])
def delete_document(filename):
    """Delete a specific document."""
    try:
        file_path = os.path.join(current_app.config['DOC_DIR'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            flash(f'Document {filename} deleted successfully.')
        else:
            flash(f'Document {filename} not found.')
    except Exception as e:
        flash(f'Error deleting document: {str(e)}')
    return redirect(url_for('general.documents'))

@general_bp.route('/api/analyze-word', methods=['GET'])
def analyze_word():
    """API to analyze a specific word."""
    word = request.args.get('word')
    doc_id = request.args.get('doc_id')
    
    if not word:
        return jsonify({'error': 'No word provided'}), 400
        
    # Lazy initialization of analyzer
    if 'word_analyzer' not in app_globals.__dict__ or app_globals.word_analyzer is None:
        app_globals.word_analyzer = WordAnalyzer(current_app.config['DATA_DIR'], current_app.config['DOC_DIR'])
        
    analysis = app_globals.word_analyzer.analyze_word(word, doc_id)
    return jsonify(analysis)
