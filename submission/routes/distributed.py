
from flask import Blueprint, render_template, request, current_app
from core.distributed.map_reduce import MapReduceIndexer
import os

distributed_bp = Blueprint('distributed', __name__)

@distributed_bp.route('/distributed/mapreduce', methods=['GET', 'POST'])
def mapreduce():
    logs = []
    index_preview = {}
    
    if request.method == 'POST':
        # Load all documents
        docs = {}
        doc_dir = current_app.config['DOC_DIR']
        if os.path.exists(doc_dir):
            for f in os.listdir(doc_dir):
                if f.endswith('.txt'):
                    with open(os.path.join(doc_dir, f), 'r', encoding='utf-8') as file:
                        docs[f] = file.read()
        
        mr = MapReduceIndexer()
        index, logs = mr.run_simulation(docs)
        
        # Preview first 10 items of index
        for k in sorted(list(index.keys()))[:10]:
            index_preview[k] = index[k]
            
    return render_template('distributed/mapreduce.html', logs=logs, index_preview=index_preview)
