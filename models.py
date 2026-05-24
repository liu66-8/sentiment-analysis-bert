import os

import torch
import torch.nn as nn
from transformers import BertModel

from config import num_labels, num_classes, bert_model_cache_dir


class SentimentModel(nn.Module):
    def __init__(self, model_name, dropout_prob, checkpoint_path=None, local_config_path=None):
        super(SentimentModel, self).__init__()

        if checkpoint_path and os.path.isfile(checkpoint_path):
            self.encoder = BertModel.from_pretrained(model_name, cache_dir=bert_model_cache_dir,
                                                      local_files_only=True)
            checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=True)
            state_dict = checkpoint.get('model_state_dict', checkpoint)
            self.load_state_dict(state_dict, strict=False)
        else:
            self.encoder = BertModel.from_pretrained(model_name, cache_dir=bert_model_cache_dir,
                                                      local_files_only=True)
            print(f"[Model] Loaded from local cache: {bert_model_cache_dir}")

        self.dropout = nn.Dropout(dropout_prob)
        self.fc = nn.Linear(self.encoder.config.hidden_size, num_labels * num_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)
        logits = self.fc(pooled_output)
        logits = logits.view((-1, num_classes, num_labels))

        return logits