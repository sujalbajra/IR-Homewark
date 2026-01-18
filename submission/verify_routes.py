
import os
import sys
import requests
import time

# Add current directory to path
sys.path.append(os.getcwd())

BASE_URL = "http://127.0.0.1:5000"

def check_endpoint(name, path, method="GET", data=None):
    try:
        url = f"{BASE_URL}{path}"
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, data=data)
        
        status = response.status_code
        if status == 200:
            print(f"[PASS] {name} ({method} {path})")
        elif status == 500:
            print(f"[FAIL] {name} ({method} {path}) - 500 Internal Server Error")
        else:
            print(f"[WARN] {name} ({method} {path}) - Status {status}")
            
    except Exception as e:
        print(f"[ERR ] {name} ({method} {path}) - Connection Error: {e}")

if __name__ == "__main__":
    print("Starting Route Verification...")
    
    # General
    check_endpoint("Dashboard", "/")
    check_endpoint("Documents", "/documents")
    
    # Foundations
    check_endpoint("Boolean Search", "/foundations/boolean")
    check_endpoint("VSM", "/foundations/vsm")
    
    # Text Analysis
    check_endpoint("Text Analysis", "/text_analysis")
    
    # Indexing
    check_endpoint("Indexing", "/indexing")
    
    # Query Proc
    check_endpoint("Wildcard", "/query/wildcard")
    check_endpoint("Spellcheck", "/query/spellcheck")
    
    # Ranking
    check_endpoint("Ranking Compare", "/ranking/compare")
    check_endpoint("PageRank", "/ranking/pagerank")
    
    # Neural
    check_endpoint("Neural Search", "/neural/search")
    
    # Evaluation
    check_endpoint("Evaluation", "/evaluation")
    
    # Web Search
    check_endpoint("Web Duplicates", "/web/duplicates")
    check_endpoint("Web Spam", "/web/spam")
    
    # NLP
    check_endpoint("LM Generate", "/lm/generate")
    check_endpoint("Tokenization", "/tokenization/demo")
    check_endpoint("Synonyms", "/synonyms/finder")
    check_endpoint("Similarity", "/similarity/compare")
    check_endpoint("Numbers", "/numbers/converter")
    check_endpoint("Romanization", "/romanization/converter")
    
    print("\nVerification Complete.")
