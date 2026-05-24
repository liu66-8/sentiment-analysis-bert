import time
import torch
from torch import nn
from torch.utils.data import DataLoader
from transformers import BertTokenizer, AdamW, get_linear_schedule_with_warmup

from config import *
from data_gen import SaDataset
from models import BertMultiLabelSentiment
from utils import AverageMeter, ExpoAverageMeter, accuracy, timestamp, save_checkpoint

def train(epoch, train_loader, model, optimizer, scheduler):
    model.train()
    criterion = nn.CrossEntropyLoss().to(device)

    batch_time = AverageMeter()
    losses = ExpoAverageMeter()
    accs = ExpoAverageMeter()

    start = time.time()

    for i_batch, batch in enumerate(train_loader):
        optimizer.zero_grad()

        # 获取数据并送入 GPU
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        targets = batch['labels'].to(device)

        # 前向传播
        outputs = model(input_ids, attention_mask)

        loss = 0
        acc = 0

        # 分别计算 20 个维度的 Loss 并累加求均值
        for idx in range(num_labels):
            loss += criterion(outputs[:, :, idx], targets[:, idx]) / num_labels
            acc += accuracy(outputs[:, :, idx], targets[:, idx]) / num_labels

        loss.backward()
        
        # 梯度裁剪（防止梯度爆炸，对 BERT 很有效）
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        scheduler.step() # 更新学习率

        # 记录状态
        losses.update(loss.item())
        batch_time.update(time.time() - start)
        accs.update(acc)

        start = time.time()

        if i_batch % print_every == 0:
            print('[{0}] Epoch: [{1}][{2}/{3}]\t'
                  'Batch Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                  'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                  'Accuracy {accs.val:.3f} ({accs.avg:.3f})'.format(timestamp(), epoch, i_batch, len(train_loader),
                                                                    batch_time=batch_time,
                                                                    loss=losses,
                                                                    accs=accs))

def valid(val_loader, model):
    model.eval()
    criterion = nn.CrossEntropyLoss().to(device)

    batch_time = AverageMeter()
    losses = AverageMeter()
    accs = AverageMeter()

    start = time.time()

    with torch.no_grad():
        for i_batch, batch in enumerate(val_loader):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            targets = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask)

            loss = 0
            acc = 0

            for idx in range(num_labels):
                loss += criterion(outputs[:, :, idx], targets[:, idx]) / num_labels
                acc += accuracy(outputs[:, :, idx], targets[:, idx]) / num_labels

            losses.update(loss.item())
            batch_time.update(time.time() - start)
            accs.update(acc)

            start = time.time()

            if i_batch % print_every == 0:
                print('Validation: [{0}/{1}]\t'
                      'Batch Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                      'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                      'Accuracy {accs.val:.3f} ({accs.avg:.3f})'.format(i_batch, len(val_loader),
                                                                        batch_time=batch_time,
                                                                        loss=losses,
                                                                        accs=accs))

    return accs.avg, losses.avg


def test(test_loader, model):
    model.eval()
    criterion = nn.CrossEntropyLoss().to(device)

    batch_time = AverageMeter()
    losses = AverageMeter()
    accs = AverageMeter()

    start = time.time()

    with torch.no_grad():
        for i_batch, batch in enumerate(test_loader):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            targets = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask)

            loss = 0
            acc = 0

            for idx in range(num_labels):
                loss += criterion(outputs[:, :, idx], targets[:, idx]) / num_labels
                acc += accuracy(outputs[:, :, idx], targets[:, idx]) / num_labels

            losses.update(loss.item())
            batch_time.update(time.time() - start)
            accs.update(acc)

            start = time.time()

            if i_batch % print_every == 0:
                print('Test: [{0}/{1}]\t'
                      'Batch Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                      'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                      'Accuracy {accs.val:.3f} ({accs.avg:.3f})'.format(i_batch, len(test_loader),
                                                                        batch_time=batch_time,
                                                                        loss=losses,
                                                                        accs=accs))

    return accs.avg, losses.avg


def main():
    print('Loading BERT tokenizer...')
    tokenizer = BertTokenizer.from_pretrained(bert_model_name)

    print('Preparing datasets...')
    train_data = SaDataset('train', tokenizer, max_seq_len)
    val_data = SaDataset('valid', tokenizer, max_seq_len)
    test_data = SaDataset('test', tokenizer, max_seq_len)

    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False, num_workers=2)
    test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False, num_workers=2)

    # 初始化 BERT 模型
    print('Building model...')
    model = BertMultiLabelSentiment(bert_model_name, dropout)
    model = model.to(device)

    # BERT 推荐使用 AdamW 和线性预热学习率衰减
    print('Building optimizer ...')
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer, 
        num_warmup_steps=int(total_steps * 0.1), 
        num_training_steps=total_steps
    )

    best_acc = 0
    epochs_since_improvement = 0

    for epoch in range(start_epoch, epochs):
        if epochs_since_improvement == 5: # BERT 收敛快，早停步数可以改小
            print("Early stopping triggered.")
            break

        # 训练
        train(epoch, train_loader, model, optimizer, scheduler)

        # 验证
        val_acc, val_loss = valid(val_loader, model)
        print('\n * ACCURACY - {acc:.3f}, LOSS - {loss:.3f}\n'.format(acc=val_acc, loss=val_loss))

        # 检查是否最佳
        is_best = val_acc > best_acc
        best_acc = max(best_acc, val_acc)

        if not is_best:
            epochs_since_improvement += 1
            print("\nEpochs since last improvement: %d\n" % (epochs_since_improvement,))
        else:
            epochs_since_improvement = 0

        # 保存权重
        save_checkpoint(epoch, model, optimizer, val_acc, is_best)

    # 在测试集上评估最终模型
    print('\n' + '=' * 60)
    print('Evaluating best model on test set...')
    test_acc, test_loss = test(test_loader, model)
    print('\n * TEST ACCURACY - {acc:.3f}, TEST LOSS - {loss:.3f}\n'.format(acc=test_acc, loss=test_loss))


if __name__ == '__main__':
    main()