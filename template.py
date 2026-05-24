import json
import os

from config import label_names

if __name__ == '__main__':
    filename = 'result.json'
    if not os.path.isfile(filename):
        print(f"错误: 找不到 {filename}，请先运行 demo.py 生成推理结果")
        exit(1)

    with open(filename, 'r', encoding='utf-8') as file:
        result = json.load(file)

    lines = []
    lines.append('# 情感分析演示结果\n')
    lines.append('以下是由 BERT 模型对验证集随机采样 10 条评论进行预测的结果：\n')

    sentiment_map = {1: '😊 正面', 0: '😐 中性', -1: '😞 负面', -2: '⚪ 未提及'}

    for i, item in enumerate(result[:10]):
        content = item['content']
        labels = item['labels']

        lines.append(f'## 样本 {i + 1}\n')
        lines.append(f'**评论内容**: {content}\n')
        lines.append('| 情感维度 | 预测结果 |')
        lines.append('|---------|---------|')

        for j, label_name in enumerate(label_names):
            sentiment = sentiment_map.get(labels[j], str(labels[j]))
            lines.append(f'| {label_name} | {sentiment} |')

        lines.append('')

    with open('README.md', 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))

    print(f'已生成 README.md，包含 {len(result[:10])} 条样本结果')
