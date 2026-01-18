import os
from pathlib import Path

# Base Paths
# Assuming config.py is in submission/
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DOC_DIR = DATA_DIR / "documents"

# External Data Paths (Centralized)
NER_DATA_DIR = DATA_DIR / "nerdata"
EMBEDDING_PATH = DATA_DIR / "nepali_embeddings.npz"
POS_DICT_PATH = DATA_DIR / "id_pos_dict.json"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
DOC_DIR.mkdir(exist_ok=True)
NER_DATA_DIR.mkdir(exist_ok=True)

# Legacy support (strings)
BASE_DIR_STR = str(BASE_DIR)
DATA_DIR_STR = str(DATA_DIR)
DOC_DIR_STR = str(DOC_DIR)

class Config:
    UPLOAD_FOLDER = str(DOC_DIR)
    DOC_DIR = str(DOC_DIR)
    DATA_DIR = str(DATA_DIR)
    NER_DATA_DIR = str(NER_DATA_DIR)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nepali-ir-secret-key-fallback'
    
    # Path constants
    QA_DATASET_PATH = os.path.join(DATA_DIR, 'qa_dataset.json')
    INTERACTIONS_PATH = os.path.join(DATA_DIR, 'interactions.json')
