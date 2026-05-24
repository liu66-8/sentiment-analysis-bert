import os
import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# --- Configure BERT models ---
bert_model_name = 'hfl/chinese-bert-wwm-ext'  # HuggingFace 模型 ID
bert_local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'bert_tokenizer')
max_seq_len = 256                      # 截断/填充的最大句子长度
min_word_freq = 3                      # 词频阈值（用于传统 jieba 方式）

# --- Configure training/optimization ---
learning_rate = 2e-5                   # BERT 微调学习率通常在 1e-5 到 5e-5 之间
batch_size = 32                        # 8GB 显存建议 32，16GB 以上可尝试 64
print_every = 100
num_labels = 20
num_classes = 4                        # number of sentimental types
save_folder = 'models'

start_epoch = 0
epochs = 10                            # BERT 通常只需要 3-10 个 epoch 即可收敛
dropout = 0.1

train_folder = 'data/ai_challenger_sentiment_analysis_trainingset_20180816'
valid_folder = 'data/ai_challenger_sentiment_analysis_validationset_20180816'
test_a_folder = 'data/ai_challenger_sentiment_analysis_testa_20180816'

train_filename = 'sentiment_analysis_trainingset.csv'
valid_filename = 'sentiment_analysis_validationset.csv'
test_a_filename = 'sentiment_analysis_testa.csv'

label_names = ['location_traffic_convenience', 'location_distance_from_business_district', 'location_easy_to_find',
               'service_wait_time', 'service_waiters_attitude', 'service_parking_convenience', 'service_serving_speed',
               'price_level', 'price_cost_effective', 'price_discount', 'environment_decoration', 'environment_noise',
               'environment_space', 'environment_cleaness', 'dish_portion', 'dish_taste', 'dish_look',
               'dish_recommendation',
               'others_overall_experience', 'others_willing_to_consume_again']
assert len(label_names) == 20