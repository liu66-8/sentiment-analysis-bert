import os

import torch
import torch.nn as nn
from transformers import AutoModel, AutoConfig
from config import num_labels, num_classes


def _load_config(model_name, local_path):
    if local_path and os.path.isfile(os.path.join(local_path, 'config.json')):
        return AutoConfig.from_pretrained(local_path)
    return AutoConfig.from_pretrained(model_name, trust_remote_code=True)


class SentimentModel(nn.Module):
    def __init__(self, model_name, dropout_prob, checkpoint_path=None, local_config_path=None):
        super(SentimentModel, self).__init__()

        config = _load_config(model_name, local_config_path)

        self.encoder = AutoModel.from_pretrained(model_name, config=config)

        self.dropout = nn.Dropout(dropout_prob)
        self.fc = nn.Linear(config.hidden_size, num_labels * num_classes)

        if checkpoint_path and os.path.isfile(checkpoint_path):
            checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=True)
            state_dict = checkpoint.get('model_state_dict', checkpoint)
            self.load_state_dict(state_dict, strict=False)

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        last_hidden_state = outputs.last_hidden_state
        cls_output = last_hidden_state[:, 0, :]
        pooled_output = self.dropout(cls_output)
        logits = self.fc(pooled_output)
        logits = logits.view((-1, num_classes, num_labels))

        return logits