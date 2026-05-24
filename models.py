import os

import torch
import torch.nn as nn
from transformers import BertModel, AutoConfig

from config import num_labels, num_classes


def _load_config(model_name, local_path):
    if local_path and os.path.isfile(os.path.join(local_path, 'config.json')):
        return AutoConfig.from_pretrained(local_path)
    return AutoConfig.from_pretrained(model_name, trust_remote_code=True)


class SentimentModel(nn.Module):
    def __init__(self, model_name, dropout_prob, checkpoint_path=None, local_config_path=None):
        super(SentimentModel, self).__init__()

        if checkpoint_path and os.path.isfile(checkpoint_path):
            config = _load_config(model_name, local_config_path)
            self.encoder = BertModel(config)
            checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=True)
            state_dict = checkpoint.get('model_state_dict', checkpoint)
            self.load_state_dict(state_dict, strict=False)
        else:
            mirrors = [
                ('https://hf-mirror.com',),
                ('https://huggingface.co',),
            ]
            last_error = None
            for mirror_url in mirrors:
                try:
                    os.environ['HF_ENDPOINT'] = mirror_url[0]
                    self.encoder = BertModel.from_pretrained(model_name)
                    print(f"[Model] Download from {mirror_url[0]} succeeded")
                    break
                except Exception as e:
                    last_error = e
                    print(f"[Model] Mirror {mirror_url[0]} failed: {e}")
                    continue
            else:
                raise RuntimeError(f"All mirrors failed. Last error: {last_error}")

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