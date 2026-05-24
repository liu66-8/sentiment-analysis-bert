import argparse
import json
import os

os.environ.setdefault('HF_ENDPOINT', 'https://hf-mirror.com')

import pandas as pd
import torch
from transformers import BertTokenizer

from config import (device, save_folder, bert_model_name, num_labels,
                    num_classes, dropout, max_seq_len, label_names)
from models import BertMultiLabelSentiment


class SentimentPredictor:
    def __init__(self, checkpoint_path=None):
        self.tokenizer = BertTokenizer.from_pretrained(bert_model_name)
        self.model = BertMultiLabelSentiment(bert_model_name, dropout)

        if checkpoint_path is None:
            checkpoint_path = os.path.join(save_folder, 'BEST_checkpoint.tar')

        checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=True)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to(device)
        self.model.eval()

        self.label_map = {3: '正面', 2: '中性', 1: '负面', 0: '未提及'}

    def predict_one(self, text):
        encoding = self.tokenizer(
            text,
            max_length=max_seq_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt',
        )

        input_ids = encoding['input_ids'].to(device)
        attention_mask = encoding['attention_mask'].to(device)

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask)
            _, preds = torch.max(outputs, 1)
            preds = preds.cpu().numpy().squeeze()

        pred_labels = (preds - 2).tolist()

        result = {}
        for i, name in enumerate(label_names):
            result[name] = {
                'label_id': pred_labels[i],
                'sentiment': self.label_map[pred_labels[i] + 2]
            }

        return result

    def predict_file(self, csv_path, content_col='content', output_path=None):
        df = pd.read_csv(csv_path)
        results = []

        for idx, row in df.iterrows():
            text = str(row[content_col])
            pred = self.predict_one(text)
            results.append({'content': text, 'predictions': pred})

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            print(f'预测结果已保存到 {output_path}')

        return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BERT 细粒度情感分析预测')
    parser.add_argument('--text', '-t', type=str, help='单条文本预测')
    parser.add_argument('--input', '-i', type=str, help='CSV 文件路径（批量预测）')
    parser.add_argument('--output', '-o', type=str, default='predictions.json', help='输出文件路径')
    parser.add_argument('--content_col', type=str, default='content', help='CSV 中的文本列名')
    args = parser.parse_args()

    predictor = SentimentPredictor()

    if args.text:
        result = predictor.predict_one(args.text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.input:
        results = predictor.predict_file(args.input, args.content_col, args.output)
        for r in results:
            print(f"文本: {r['content'][:50]}...")
            print(f"预测: {r['predictions']}")
            print('-' * 50)
    else:
        print("请使用 --text 指定单条文本 或 --input 指定 CSV 文件路径")
