import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('HF_ENDPOINT', 'https://hf-mirror.com')
os.environ.setdefault('HF_HUB_ENABLE_HF_TRANSFER', '0')

from config import (
    device, save_folder, bert_model_name, num_labels, num_classes,
    dropout, max_seq_len, label_names
)

DATABASE_URL = "sqlite:///sentiment.db"
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
MAX_BATCH_SIZE = 5000
MAX_FILE_SIZE_MB = 10
