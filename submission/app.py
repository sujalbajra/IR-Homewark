from flask import Flask, render_template
from config import Config
import os
import json
from extensions import app_globals

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure data directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize globals (if any explicit init needed, otherwise handled in routes by usage)
    # Ideally extensions are initialized here if they were proper Flask-Extensions

    # Register Blueprints
    from routes.general import general_bp
    from routes.foundations import foundations_bp
    from routes.text_analysis import text_analysis_bp
    from routes.indexing import indexing_bp
    from routes.query_proc import query_proc_bp
    from routes.ranking import ranking_bp
    from routes.neural import neural_bp
    from routes.evaluation import evaluation_bp
    from routes.web_search import web_search_bp
    from routes.web_search import web_search_bp
    from routes.nlp import nlp_bp
    from routes.ml_training import ml_bp
    from routes.distributed import distributed_bp
    from routes.clir import clir_bp
    from routes.ethics import ethics_bp

    app.register_blueprint(general_bp)
    app.register_blueprint(foundations_bp)
    app.register_blueprint(text_analysis_bp)
    app.register_blueprint(indexing_bp)
    app.register_blueprint(query_proc_bp)
    app.register_blueprint(ranking_bp)
    app.register_blueprint(neural_bp)
    app.register_blueprint(evaluation_bp)
    app.register_blueprint(web_search_bp)
    app.register_blueprint(nlp_bp)
    app.register_blueprint(ml_bp)
    app.register_blueprint(distributed_bp)
    app.register_blueprint(clir_bp)
    app.register_blueprint(ethics_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
