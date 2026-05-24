import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import torch
from transformers import BertTokenizer, AutoConfig

from config import device, save_folder, bert_model_name, bert_local_path, dropout, max_seq_len, label_names
from models import BertMultiLabelSentiment

LABEL_MAP = {3: '正面', 2: '中性', 1: '负面', 0: '未提及'}

LABEL_CATEGORIES = {
    'location_traffic_convenience': '位置',
    'location_distance_from_business_district': '位置',
    'location_easy_to_find': '位置',
    'service_wait_time': '服务',
    'service_waiters_attitude': '服务',
    'service_parking_convenience': '服务',
    'service_serving_speed': '服务',
    'price_level': '价格',
    'price_cost_effective': '价格',
    'price_discount': '价格',
    'environment_decoration': '环境',
    'environment_noise': '环境',
    'environment_space': '环境',
    'environment_cleaness': '环境',
    'dish_portion': '菜品',
    'dish_taste': '菜品',
    'dish_look': '菜品',
    'dish_recommendation': '菜品',
    'others_overall_experience': '整体',
    'others_willing_to_consume_again': '整体',
}

LABEL_DISPLAY_NAMES = {
    'location_traffic_convenience': '交通便利性',
    'location_distance_from_business_district': '距商圈距离',
    'location_easy_to_find': '是否容易找到',
    'service_wait_time': '排队等候时间',
    'service_waiters_attitude': '服务员态度',
    'service_parking_convenience': '停车便利性',
    'service_serving_speed': '上菜速度',
    'price_level': '价格水平',
    'price_cost_effective': '性价比',
    'price_discount': '折扣力度',
    'environment_decoration': '装修风格',
    'environment_noise': '环境噪音',
    'environment_space': '空间大小',
    'environment_cleaness': '环境卫生',
    'dish_portion': '菜品分量',
    'dish_taste': '菜品口味',
    'dish_look': '菜品外观',
    'dish_recommendation': '是否推荐',
    'others_overall_experience': '整体体验',
    'others_willing_to_consume_again': '是否会再次消费',
}


def _is_local_tokenizer_ready(path):
    return (
        os.path.isfile(os.path.join(path, 'tokenizer_config.json'))
        and os.path.isfile(os.path.join(path, 'vocab.txt'))
    )


def _download_file(url, dest_path):
    import urllib.request
    print(f"[Download] Downloading {url} to {dest_path}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"[Download] Successfully downloaded {dest_path}")
    except Exception as e:
        print(f"[Download] Failed to download: {e}")
        raise

def _load_tokenizer(source_name, local_path):
    print(f"[Init] Loading BERT tokenizer...")
    if _is_local_tokenizer_ready(local_path):
        print(f"[Init] Loading from local: {local_path}")
        return BertTokenizer.from_pretrained(local_path)
    print(f"[Init] Local files not found. Trying to download...")
    mirrors = [
        os.environ.get('HF_ENDPOINT', 'https://hf-mirror.com'),
        'https://hf.xeduapi.com',
    ]
    last_error = None
    for mirror in mirrors:
        try:
            print(f"[Init] Trying mirror: {mirror}")
            os.environ['HF_ENDPOINT'] = mirror
            tok = BertTokenizer.from_pretrained(source_name)
            print(f"[Init] OK - tokenizer loaded via {mirror}")
            return tok
        except Exception as e:
            last_error = e
            print(f"[Init] Mirror failed: {e}")
            continue
    raise RuntimeError(
        f"Tokenizer download failed from all mirrors.\n"
        f"Please run: python download_tokenizer.py\n"
        f"Last error: {last_error}"
    )


class SentimentPredictor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        import time
        t0 = time.time()

        self.device = device
        self.tokenizer = _load_tokenizer(bert_model_name, bert_local_path)
        print(f"[Init] Tokenizer loaded ({time.time()-t0:.1f}s)")

        t1 = time.time()
        light_ckpt = os.path.join(save_folder, 'BEST_checkpoint_inference.tar')
        full_ckpt = os.path.join(save_folder, 'BEST_checkpoint.tar')

        if os.path.isfile(light_ckpt):
            checkpoint_path = light_ckpt
            print(f"[Init] Using lightweight checkpoint ({os.path.getsize(light_ckpt)/1024/1024:.0f}MB)")
        elif os.path.isfile(full_ckpt):
            checkpoint_path = full_ckpt
            print(f"[Init] Using full checkpoint ({os.path.getsize(full_ckpt)/1024/1024:.0f}MB)")
            print("[Init] Tip: run 'python convert_checkpoint.py' to create a lighter version for faster startup")
        else:
            print(f"[Init] No checkpoint found in {save_folder}, using pre-trained model...")
            checkpoint_path = None
            print("[Init] Using HuggingFace pre-trained model without fine-tuning")

        self.model = BertMultiLabelSentiment(bert_model_name, dropout, checkpoint_path=checkpoint_path,
                                              local_config_path=bert_local_path)
        print(f"[Init] Model loaded ({time.time()-t1:.1f}s)")

        t2 = time.time()
        self.model = self.model.to(self.device)
        self.model.eval()
        print(f"[Init] Model moved to {self.device} ({time.time()-t2:.1f}s)")
        print(f"[Init] Total startup: {time.time()-t0:.1f}s")

    def predict_one(self, text):
        encoding = self.tokenizer(
            text,
            max_length=max_seq_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt',
        )

        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask)
            _, preds = torch.max(outputs, 1)
            preds = preds.cpu().numpy().squeeze()

        pred_labels = (preds - 2).tolist()

        result = {}
        for i, name in enumerate(label_names):
            result[name] = {
                'label_id': pred_labels[i],
                'sentiment': LABEL_MAP.get(pred_labels[i] + 2, '未知'),
                'display_name': LABEL_DISPLAY_NAMES.get(name, name),
                'category': LABEL_CATEGORIES.get(name, '其他'),
            }

        summary = self._build_summary(pred_labels)
        suggestions = self._build_suggestions(text, result, summary)

        return result, summary, suggestions

    def _build_summary(self, labels):
        counts = {'正面': 0, '中性': 0, '负面': 0, '未提及': 0}
        for label_id in labels:
            sentiment = LABEL_MAP.get(label_id + 2, '未提及')
            counts[sentiment] += 1
        return counts

    def _build_suggestions(self, text, result, summary):
        try:
            from backend.services.llm_suggestions import generate_llm_suggestions
            llm_result = generate_llm_suggestions(text, result, summary)
            if llm_result:
                return llm_result
        except Exception:
            pass
        return None


predictor = SentimentPredictor()
