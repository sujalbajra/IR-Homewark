
from flask import Blueprint, render_template, request, jsonify, current_app
from core.ch22_word2vec_model import Word2VecNumPy
from core.ch23_neural_classifier import DocumentClassifierPT
from extensions import app_globals
import os

ml_bp = Blueprint('ml', __name__)

@ml_bp.route('/ml/word2vec/train', methods=['GET', 'POST'])
def train_word2vec():
    """Train Word2Vec Model"""
    if request.method == 'POST':
        embedding_dim = int(request.form.get('embedding_dim', 100))
        epochs = int(request.form.get('epochs', 5))
        vocab_size = int(request.form.get('vocab_size', 5000))
        
        # Load corpus
        corpus = []
        doc_dir = current_app.config['DOC_DIR']
        for f in os.listdir(doc_dir):
            if f.endswith('.txt'):
                with open(os.path.join(doc_dir, f), 'r', encoding='utf-8') as file:
                    corpus.append(file.read())
                    
        model = Word2VecNumPy(vocab_size=vocab_size, embedding_dim=embedding_dim)
        history = model.train(corpus, epochs=epochs)
        
        # Save model
        save_path = os.path.join(current_app.config['DATA_DIR'], 'word2vec_model.pkl')
        model.save_model(save_path)
        
        return jsonify({'status': 'success', 'history': history, 'message': 'Model trained and saved!'})
        
    return render_template('ml/word2vec_train.html')

@ml_bp.route('/ml/classifier/train', methods=['GET', 'POST'])
def train_classifier():
    """Train Document Classifier"""
    if request.method == 'POST':
        epochs = int(request.form.get('epochs', 10))
        
        # Load docs and inferred labels (from filename conventions doc011_politics.txt)
        documents = []
        labels = []
        doc_dir = current_app.config['DOC_DIR']
        
        for f in os.listdir(doc_dir):
            if f.endswith('.txt'):
                parts = f.split('_')
                if len(parts) > 1:
                    label = parts[1].replace('.txt', '') # politics
                    with open(os.path.join(doc_dir, f), 'r', encoding='utf-8') as file:
                        documents.append(file.read())
                        labels.append(label)
                        
        if len(set(labels)) < 2:
            return jsonify({'status': 'error', 'message': 'Need at least 2 categories of documents (e.g., _politics, _sports)'})
            
        # Initialize global model if not exists
        if app_globals.classifier is None:
            app_globals.classifier = DocumentClassifierPT()
            
        history = app_globals.classifier.train(documents, labels, epochs=epochs)
        
        return jsonify({
            'status': 'success', 
            'history': history, 
            'classes': app_globals.classifier.classes,
            'message': f'Model trained on {len(documents)} documents across {len(set(labels))} classes'
        })
        
    return render_template('ml/classifier_train.html')

@ml_bp.route('/ml/classifier/retrain', methods=['POST'])
def retrain_classifier():
    """Retrain on new document"""
    text = request.form.get('text')
    label = request.form.get('label')
    
    if app_globals.classifier is None:
        return jsonify({'status': 'error', 'message': 'Train a base model first!'})
        
    history = app_globals.classifier.retrain([text], [label], epochs=5)
    
    return jsonify({
        'status': 'success',
        'history': history,
        'message': f'Model updated with new {label} document'
    })

@ml_bp.route('/ml/predict', methods=['POST'])
def predict_classifier():
    """Predict category"""
    text = request.form.get('text')
    if app_globals.classifier is None:
        return jsonify({'status': 'error', 'message': 'Model not trained'})
        
    category = app_globals.classifier.predict(text)
    return jsonify({'category': category})
