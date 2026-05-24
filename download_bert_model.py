import os
import sys

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'bert_model_cache')

MODEL_NAME = 'bert-base-chinese'

os.makedirs(CACHE_DIR, exist_ok=True)

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['TRANSFORMERS_CACHE'] = CACHE_DIR
os.environ['HF_HOME'] = CACHE_DIR

print(f"[Build] Downloading model: {MODEL_NAME}")
print(f"[Build] Cache dir: {CACHE_DIR}")
print(f"[Build] Using mirror: https://hf-mirror.com")

try:
    from transformers import BertModel, BertTokenizer
    bert = BertModel.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
    print("[Build] BertModel downloaded successfully")
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
    print("[Build] BertTokenizer downloaded successfully")
    print(f"[Build] Files in cache:")
    for root, dirs, files in os.walk(CACHE_DIR):
        for f in files:
            filepath = os.path.join(root, f)
            size_mb = os.path.getsize(filepath) / 1024 / 1024
            print(f"  {filepath} ({size_mb:.1f}MB)")
    print("[Build] Model download complete!")
except Exception as e:
    print(f"[Build] Mirror failed: {e}")
    print("[Build] Trying direct download from huggingface.co...")
    os.environ['HF_ENDPOINT'] = 'https://huggingface.co'
    from transformers import BertModel, BertTokenizer
    bert = BertModel.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
    print("[Build] Model downloaded from huggingface.co")
