from flask import Blueprint, render_template, request, current_app

nlp_bp = Blueprint('nlp', __name__)

@nlp_bp.route('/lm/generate', methods=['GET', 'POST'])
def lm_generate():
    """N-gram Language Model text generation"""
    from core.ch14_language_model import NepaliNgramLM
    
    generated = None
    predictions = None
    seed = None
    n = 2
    max_words = 15
    stats = None
    
    if request.method == 'POST':
        seed = request.form.get('seed')
        n = int(request.form.get('n', 2))
        max_words = int(request.form.get('max_words', 15))
        
        # Load corpus and train model
        # Note: Paths should be absolute or relative to base dir. 
        # Ideally passed via config, but keeping simple for now.
        with open('data/nepali_corpus.txt', 'r', encoding='utf-8') as f:
            corpus = f.read().split('\n')
        
        lm = NepaliNgramLM(n=n)
        lm.train(corpus)
        
        # Generate text
        generated = lm.generate(seed, max_words=max_words)
        
        # Get predictions
        predictions = lm.predict_next(seed, top_k=5)
        
        # Get model stats
        stats = lm.get_stats()
    
    return render_template('lm/generate.html', 
                         generated=generated, 
                         predictions=predictions,
                         seed=seed,
                         n=n,
                         max_words=max_words,
                         stats=stats)

@nlp_bp.route('/tokenization/demo', methods=['GET', 'POST'])
def tokenization_demo():
    """Enhanced Nepali tokenization"""
    from core.ch15_tokenization import NepaliTokenizer
    
    results = None
    text = None
    level = 'all'
    
    if request.method == 'POST':
        text = request.form.get('text')
        level = request.form.get('level', 'all')
        
        tokenizer = NepaliTokenizer()
        results = {}
        
        if level in ['all', 'sentence']:
            results['sentences'] = tokenizer.sentence_tokenize(text)
        
        if level in ['all', 'word']:
            results['words'] = tokenizer.word_tokenize(text)
        
        if level in ['all', 'ngram']:
            words = tokenizer.word_tokenize(text)
            results['bigrams'] = tokenizer.generate_ngrams(words, n=2)
            results['trigrams'] = tokenizer.generate_ngrams(words, n=3)
        
        if level == 'all':
            results['stats'] = tokenizer.get_statistics(text)
    
    return render_template('tokenization/demo.html', results=results, text=text, level=level)

@nlp_bp.route('/synonyms/finder', methods=['GET', 'POST'])
def synonyms_finder():
    """Find synonyms using word embeddings"""
    from core.ch16_synonyms import NepaliSynonyms
    
    synonyms = None
    word = None
    top_k = 5
    vocab_size = 0
    sample_vocab = []
    
    if request.method == 'POST':
        word = request.form.get('word')
        top_k = int(request.form.get('top_k', 5))
        
        finder = NepaliSynonyms()
        vocab_size = len(finder.get_vocabulary())
        sample_vocab = finder.get_vocabulary()[:50]
        
        synonyms = finder.find_synonyms(word, top_k=top_k)
    
    return render_template('synonyms/finder.html', 
                         synonyms=synonyms, 
                         word=word, 
                         top_k=top_k,
                         vocab_size=vocab_size,
                         sample_vocab=sample_vocab)

@nlp_bp.route('/similarity/compare', methods=['GET', 'POST'])
def similarity_compare():
    """Compare sentence similarity"""
    from core.ch17_similarity import NepaliSimilarity
    
    scores = None
    sent1 = None
    sent2 = None
    
    if request.method == 'POST':
        sent1 = request.form.get('sent1')
        sent2 = request.form.get('sent2')
        
        similarity = NepaliSimilarity()
        scores = similarity.compare_all(sent1, sent2)
    
    return render_template('similarity/compare.html', 
                         scores=scores, 
                         sent1=sent1, 
                         sent2=sent2)

@nlp_bp.route('/numbers/converter', methods=['GET', 'POST'])
def numbers_converter():
    """Nepali number conversion"""
    from core.ch18_nepali_numbers import NepaliNumber
    
    results = None
    number = None
    conversion_type = 'all'
    
    if request.method == 'POST':
        number = request.form.get('number')
        conversion_type = request.form.get('conversion_type', 'all')
        
        try:
            num = int(number)
            converter = NepaliNumber()
            results = {}
            
            if conversion_type in ['all', 'digits']:
                results['nepali_digits'] = converter.to_nepali_digits(num)
            
            if conversion_type in ['all', 'words']:
                results['nepali_words'] = converter.to_nepali_words(num)
            
            if conversion_type in ['all', 'format']:
                results['formatted_nepali'] = converter.format_with_commas(num, use_nepali_digits=True)
                results['formatted_english'] = converter.format_with_commas(num, use_nepali_digits=False)
        except ValueError:
            results = {'error': 'Invalid number'}
    
    return render_template('numbers/converter.html', 
                         results=results, 
                         number=number,
                         conversion_type=conversion_type)

@nlp_bp.route('/romanization/converter', methods=['GET', 'POST'])
def romanization_converter():
    """Romanization Converter"""
    from core.ch19_romanization import NepaliRomanization
    
    result = None
    text = None
    direction = 'to_nepali'
    
    if request.method == 'POST':
        text = request.form.get('text')
        direction = request.form.get('direction', 'to_nepali')
        
        converter = NepaliRomanization()
        
        if direction == 'to_nepali':
            result = converter.romanize_to_nepali(text)
        else:
            result = converter.nepali_to_roman(text)
            
    return render_template('romanization/converter.html', 
                         result=result, 
                         text=text,
                         direction=direction)

@nlp_bp.route('/readability/score', methods=['GET', 'POST'])
def readability_score():
    """Nepali Readability Score Calculator"""
    from core.ch20_readability import NepaliReadability
    import os
    
    results = None
    text = None
    
    if request.method == 'POST':
        text = request.form.get('text')
        
        # Path to dictionary copied from experiment
        dict_path = os.path.join(current_app.config['DATA_DIR'], 'final_token_counts.csv')
        
        analyzer = NepaliReadability(dictionary_path=dict_path)
        if text:
            results = analyzer.analyze_text(text)
            
    return render_template('nlp/readability.html', results=results, text=text)
