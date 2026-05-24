import os

import torch
import torch.nn as nn


class SimpleSentimentModel(nn.Module):
    def __init__(self, vocab_size=21128, embedding_dim=128, hidden_dim=256, num_labels=20, num_classes=4):
        super(SimpleSentimentModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(0.1)
        self.fc = nn.Linear(hidden_dim * 2, num_labels * num_classes)
        self.num_classes = num_classes
        self.num_labels = num_labels

    def forward(self, input_ids, attention_mask):
        embedded = self.embedding(input_ids)
        lstm_out, _ = self.lstm(embedded)
        cls_output = lstm_out[:, 0, :]
        pooled = self.dropout(cls_output)
        logits = self.fc(pooled)
        logits = logits.view((-1, self.num_classes, self.num_labels))
        return logits


class SentimentModel:
    def __init__(self, model_name=None, dropout_prob=0.1, checkpoint_path=None, local_config_path=None):
        self.model = SimpleSentimentModel()
        self.model.eval()
        print("[Model] Using simple LSTM model")

    def to(self, device):
        self.model = self.model.to(device)
        return self

    def eval(self):
        self.model.eval()

    def __call__(self, input_ids, attention_mask):
        return self.model(input_ids, attention_mask)