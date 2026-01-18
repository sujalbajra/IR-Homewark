from flask import Blueprint, render_template, request
from core.ch07_evaluation import Evaluation

evaluation_bp = Blueprint('evaluation', __name__)

@evaluation_bp.route('/evaluation', methods=['GET', 'POST'])
def evaluation_demo():
    metrics = None
    selected_query = None
    
    # Predefined scenarios for 5 queries (Ground Truth vs System Output)
    scenarios = {
        'q1': {
            'query': 'सेयर बजार (Share Market)',
            'relevant': ['train0014', 'train0050', 'train0002'],
            'retrieved': ['train0014', 'train0050', 'train0015'], # 2 TP, 1 FP, 1 FN
            'description': 'Business news query. System retrieves 2 relevant docs but misses one about price drop.'
        },
        'q2': {
            'query': 'क्रिकेट (Cricket)',
            'relevant': ['train0013', 'train0022', 'train0035', 'train0038'],
            'retrieved': ['train0013', 'train0022', 'train0038', 'train0006', 'train0007'], # 3 TP, 2 FP (Football)
            'description': 'Sports query. System confuses Football matches (train0006, 0007) with Cricket.'
        },
        'q3': {
            'query': 'चलचित्र (Movies)',
            'relevant': ['train0001', 'train0005', 'train0039', 'train0029'],
            'retrieved': ['train0001', 'doc001', 'doc002', 'train0039'], # 2 TP, 2 FP (Noise)
            'description': 'Entertainment query. Retrieval affected by noisy documents (doc001, doc002).'
        },
        'q4': {
            'query': 'अन्तरिक्ष (Space)',
            'relevant': ['train0004'],
            'retrieved': ['train0004', 'train0016'], # 1 TP, 1 FP
            'description': 'Specific Science query. High precision required.'
        },
        'q5': {
            'query': 'प्रधानमन्त्री (Prime Minister)',
            'relevant': ['train0009', 'train0031'],
            'retrieved': ['train0009', 'train0030', 'train0031'], # 2 TP, 1 FP (PM Cup - Sports)
            'description': 'Entity query. System retrieves "Prime Minister Cup" (Sports) incorrectly.'
        }
    }
    
    if request.method == 'POST':
        query_id = request.form.get('query_id')
        
        # Handle Manual Calculation
        if 'tp' in request.form:
            try:
                tp = int(request.form.get('tp', 0))
                fp = int(request.form.get('fp', 0))
                fn = int(request.form.get('fn', 0))
                
                prec = tp / (tp + fp) if (tp + fp) > 0 else 0
                rec = tp / (tp + fn) if (tp + fn) > 0 else 0
                f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0
                
                metrics = {
                    'precision': prec,
                    'recall': rec,
                    'f1': f1,
                    'mode': 'manual',
                    'tp': tp, 'fp': fp, 'fn': fn
                }
            except ValueError:
                pass
                
        # Handle Scenario Selection
        elif query_id and query_id in scenarios:
            selected_query = query_id
            scenario = scenarios[query_id]
            retrieved = scenario['retrieved']
            relevant = scenario['relevant']
            
            evaluator = Evaluation()
            prec = evaluator.precision(retrieved, relevant)
            rec = evaluator.recall(retrieved, relevant)
            f1 = evaluator.f1_score(prec, rec)
            ap = evaluator.average_precision(retrieved, relevant)
            
            # Calculate TP, FP, FN for display
            tp_set = set(retrieved) & set(relevant)
            tp = len(tp_set)
            fp = len(set(retrieved) - set(relevant))
            fn = len(set(relevant) - set(retrieved))
            
            metrics = {
                'precision': prec,
                'recall': rec,
                'f1': f1,
                'ap': ap,
                'retrieved': retrieved,
                'relevant': relevant,
                'tp': tp,
                'fp': fp,
                'fn': fn,
                'mode': 'scenario',
                'description': scenario['description'],
                'query_text': scenario['query'],
                'tp_list': list(tp_set)
            }

    return render_template('evaluation/metrics.html', metrics=metrics, scenarios=scenarios, selected_query=selected_query)
