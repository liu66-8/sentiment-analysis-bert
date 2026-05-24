import json
import os
import random

os.environ.setdefault('HF_ENDPOINT', 'https://hf-mirror.com')

import pandas as pd
import torch
from transformers import BertTokenizer

from config import (device, save_folder, valid_folder, valid_filename,
                    bert_model_name, num_labels, num_classes, dropout, max_seq_len, label_names)
from data_gen import parse_user_reviews
from models import BertMultiLabelSentiment

if __name__ == '__main__':
    tokenizer = BertTokenizer.from_pretrained(bert_model_name)

    model = BertMultiLabelSentiment(bert_model_name, dropout)
    checkpoint_path = '{}/BEST_checkpoint.tar'.format(save_folder)
    print('Loading checkpoint: ' + str(checkpoint_path))
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=True)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()

    filename = os.path.join(valid_folder, valid_filename)
    user_reviews = pd.read_csv(filename)
    samples = parse_user_reviews(user_reviews)
    samples = random.sample(samples, 10)

    result = []

    with torch.no_grad():
        for i, sample in enumerate(samples):
            content = sample['content']
            label_tensor = sample['label_tensor']

            encoding = tokenizer(
                content,
                max_length=max_seq_len,
                padding='max_length',
                truncation=True,
                return_tensors='pt',
            )

            input_ids = encoding['input_ids'].to(device)
            attention_mask = encoding['attention_mask'].to(device)

            outputs = model(input_ids, attention_mask)
            _, preds = torch.max(outputs, 1)
            preds = preds.cpu().numpy().squeeze()

            pred_labels = (preds - 2).tolist()
            true_labels = (label_tensor - 2).tolist()

            result.append({
                'content': content,
                'labels': pred_labels
            })

            correct_count = sum(1 for p, t in zip(pred_labels, true_labels) if p == t)
            print(f"--- 样本 {i + 1} ---")
            print(f"评论: {content[:80]}...")
            print(f"预测: {pred_labels}")
            print(f"真实: {true_labels}")
            print(f"维度准确: {correct_count}/{num_labels}")
            print()

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print(f"结果已保存到 result.json，共 {len(result)} 条样本")
