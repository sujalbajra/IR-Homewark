
import os
import json
import random
import networkx as nx
from pathlib import Path

# Nepali dummy data content
CATEGORIES = ['politics', 'sports', 'technology', 'culture', 'travel']

NEPALI_WORDS = {
    'politics': ['सरकार', 'मन्त्री', 'चुनाव', 'संसद', 'राजनीति', 'नेता', 'दल', 'संविधान', 'लोकतन्त्र', 'अधिकार'],
    'sports': ['खेल', 'फुटबल', 'क्रिकेट', 'खेलाडी', 'मैदान', 'गोल', 'जित', 'हार', 'प्रतियोगिता', 'टिम'],
    'technology': ['कम्प्युटर', 'मोबाइल', 'इन्टरनेट', 'प्रविधि', 'सफ्टवेयर', 'डाटा', 'डिजिटल', 'नेटवर्क', 'कोड', 'नयाँ'],
    'culture': ['संस्कृति', 'चाडपर्व', 'दशैं', 'तिहार', 'मन्दिर', 'जात्रा', 'परम्परा', 'कला', 'धर्म', 'इतिहास'],
    'travel': ['यात्रा', 'पर्यटन', 'हिमाल', 'पोखरा', 'लुम्बिनी', 'होटल', 'विमान', 'दृश्य', 'मार्गति', 'साहस']
}

COMMON_WORDS = ['छ', 'र', 'को', 'मा', 'यो', 'पनि', 'नेपाल', 'आज', 'भयो', 'गर्ने', 'हुने', 'धेरै', 'राम्रो']

TEMPLATES = [
    "नेपालको {cat} क्षेत्रमा {word1} र {word2} को महत्व धेरै छ।",
    "{word1} ले {cat} विकासमा ठूलो भूमिका खेल्छ।",
    "आज {word1} को बारेमा चर्चा भयो, जसमा {word2} पनि समावेश छ।",
    "{word1} र {word2} बिना {cat} अपुरो हुन्छ।",
    "हामीले {word1} को संरक्षण गर्नुपर्छ।",
    "{cat} मा {word1} को प्रयोग बढ्दै छ।",
    "यो {word1} ले {word2} लाई सहयोग पुर्याउँछ।",
    "{word1} को विकासले देश विकास हुन्छ।"
]

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def generate_text(category, length=10):
    words = NEPALI_WORDS[category] + COMMON_WORDS
    text = []
    for _ in range(length):
        template = random.choice(TEMPLATES)
        sentence = template.format(
            cat=category,
            word1=random.choice(words),
            word2=random.choice(words)
        )
        text.append(sentence)
    return " ".join(text)

def generate_documents(base_dir, count=50):
    ensure_dir(os.path.join(base_dir, 'documents'))
    metadata = {}
    
    print(f"Generating {count} documents...")
    
    for i in range(1, count + 1):
        doc_id = f"doc{i:03d}"
        category = random.choice(CATEGORIES)
        content = generate_text(category, length=random.randint(5, 15))
        
        # Save .txt file
        with open(os.path.join(base_dir, 'documents', f"{doc_id}.txt"), 'w', encoding='utf-8') as f:
            f.write(content)
            
        # Add to metadata
        metadata[doc_id] = {
            "title": f"Document {doc_id}",
            "author": f"Author {random.randint(1, 10)}",
            "date": f"2025-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "category": category,
            "length": len(content.split())
        }
        
    # Save metadata.json
    with open(os.path.join(base_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    return list(metadata.keys())

def generate_web_graph(base_dir, doc_ids):
    print("Generating web graph...")
    # Create a random graph using Barabasi-Albert model (preferential attachment like standard web)
    G = nx.scale_free_graph(len(doc_ids))
    
    graph_data = {"nodes": [], "edges": []}
    
    # Map graph indices to doc IDs
    node_map = {i: doc_id for i, doc_id in enumerate(doc_ids)}
    
    for idx, doc_id in node_map.items():
        graph_data["nodes"].append({"id": doc_id})
        
    for u, v in G.edges():
        if u in node_map and v in node_map and u != v:
            # Add some randomness to reduce edges if too dense
            if random.random() > 0.5:
                graph_data["edges"].append({
                    "source": node_map[u],
                    "target": node_map[v]
                })
                
    with open(os.path.join(base_dir, 'web_graph.json'), 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2)

def generate_qa_pairs(base_dir, doc_ids):
    print("Generating QA dataset...")
    qa_data = []
    
    # Simple heuristic generation
    for _ in range(20):
        doc_id = random.choice(doc_ids)
        # In real scenario, we'd extract actual text. Here we simulate.
        qa_data.append({
            "id": f"qa_{random.randint(1000, 9999)}",
            "question": f"Question regarding {doc_id} content?",
            "answer": "Simulated answer",
            "relevant_doc": doc_id
        })
        
    with open(os.path.join(base_dir, 'qa_dataset.json'), 'w', encoding='utf-8') as f:
        json.dump(qa_data, f, indent=2)

def generate_stopwords(base_dir):
    print("Generating stopwords...")
    # Simple Nepali stopwords list
    stopwords = ["छ", "र", "को", "मा", "म", "तिमी", "यो", "त्यो", "पनि", "सबै", "लाई", "ले", "बाट", "हो", "तथा", "भने", "गरे", "गर्ने", "छन्", "थियो"] # Expanded list in real app
    
    with open(os.path.join(base_dir, 'stopwords.txt'), 'w', encoding='utf-8') as f:
        f.write("\n".join(stopwords))

def main():
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    ensure_dir(base_dir)
    
    doc_ids = generate_documents(base_dir)
    generate_web_graph(base_dir, doc_ids)
    generate_qa_pairs(base_dir, doc_ids)
    generate_stopwords(base_dir)
    
    print(f"Data generation complete! Check {base_dir}")

if __name__ == "__main__":
    main()
