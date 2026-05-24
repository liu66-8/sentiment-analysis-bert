import datetime
import os
import time
import torch
import pandas as pd
from config import *

class AverageMeter(object):
    """ Keeps track of most recent, average, sum, and count of a metric. """
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

class ExpoAverageMeter(object):
    """ Exponential Weighted Average Meter """
    def __init__(self, beta=0.9):
        self.reset()

    def reset(self):
        self.beta = 0.9
        self.val = 0
        self.avg = 0
        self.count = 0

    def update(self, val):
        self.val = val
        self.avg = self.beta * self.avg + (1 - self.beta) * self.val

def adjust_learning_rate(optimizer, shrink_factor):
    print("\nDECAYING learning rate.")
    for param_group in optimizer.param_groups:
        param_group['lr'] = param_group['lr'] * shrink_factor
    print("The new learning rate is %f\n" % (optimizer.param_groups[0]['lr'],))

def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def save_checkpoint(epoch, model, optimizer, val_acc, is_best):
    ensure_folder(save_folder)
    
    state = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'val_acc': val_acc
    }

    if is_best:
        filename = '{0}/checkpoint_{1}_{2:.3f}.tar'.format(save_folder, epoch, val_acc)
        torch.save(state, filename)
        torch.save(state, '{}/BEST_checkpoint.tar'.format(save_folder))
        torch.save({'model_state_dict': model.state_dict()},
                   '{}/BEST_checkpoint_inference.tar'.format(save_folder))

def accuracy(scores, targets, k=1):
    batch_size = targets.size(0)
    _, ind = scores.topk(k, 1, True, True)
    correct = ind.eq(targets.view(-1, 1).expand_as(ind))
    correct_total = correct.view(-1).float().sum()
    return correct_total.item() * (100.0 / batch_size)

def parse_user_reviews(split):
    if split == 'train':
        filename = os.path.join(train_folder, train_filename)
    elif split == 'valid':
        filename = os.path.join(valid_folder, valid_filename)
    else:
        filename = os.path.join(test_a_folder, test_a_filename)
    user_reviews = pd.read_csv(filename)
    return user_reviews

def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')