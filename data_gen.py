import os
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset
from config import *

# Meaning	    Positive	Neutral	    Negative	Not mentioned
# Old labels    1	        0	        -1	        -2
# New labels    3           2           1           0
def map_sentimental_type(value):
    return value + 2

def parse_user_reviews(user_reviews):
    samples = []
    for i in range(len(user_reviews)):
        content = str(user_reviews['content'][i])
        label_tensor = np.empty((num_labels,), dtype=np.int32)
        for idx, name in enumerate(label_names):
            sentimental_type = user_reviews[name][i]
            y = map_sentimental_type(sentimental_type)
            label_tensor[idx] = y
        samples.append({'content': content, 'label_tensor': label_tensor})
    return samples

class SaDataset(Dataset):
    def __init__(self, split, tokenizer, max_len):
        self.split = split
        self.tokenizer = tokenizer
        self.max_len = max_len
        assert self.split in {'train', 'valid', 'test'}

        if split == 'train':
            filename = os.path.join(train_folder, train_filename)
        elif split == 'valid':
            filename = os.path.join(valid_folder, valid_filename)
        else:
            filename = os.path.join(test_a_folder, test_a_filename)

        user_reviews = pd.read_csv(filename)
        self.samples = parse_user_reviews(user_reviews)

    def __getitem__(self, i):
        content = self.samples[i]['content']
        labels = self.samples[i]['label_tensor']

        # 使用 BERT Tokenizer 进行编码、截断和填充
        encoding = self.tokenizer(
            content,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(labels, dtype=torch.long)
        }

    def __len__(self):
        return len(self.samples)