import os
import urllib.request
import tarfile

MODEL_URL = "https://huggingface.co/liu66-8/sentiment-analysis-bert/resolve/main/models/BEST_checkpoint_inference.tar"
MODEL_PATH = "models/BEST_checkpoint_inference.tar"

def download_model():
    if os.path.isfile(MODEL_PATH):
        print(f"[Download] Model already exists: {MODEL_PATH}")
        return
    
    os.makedirs("models", exist_ok=True)
    print(f"[Download] Downloading model from {MODEL_URL}")
    
    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print(f"[Download] Model downloaded successfully: {MODEL_PATH}")
        
        if MODEL_PATH.endswith('.tar'):
            print("[Download] Extracting model...")
            with tarfile.open(MODEL_PATH, 'r') as tar:
                tar.extractall('models/')
            print("[Download] Model extracted successfully")
    except Exception as e:
        print(f"[Download] Failed to download model: {e}")
        raise

if __name__ == "__main__":
    download_model()