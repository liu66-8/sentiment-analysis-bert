import os
import sys
import shutil
import glob

TOKENIZER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'bert_tokenizer')

FILES = ['tokenizer_config.json', 'vocab.txt', 'config.json']

CACHE_BASE = os.path.expanduser('~/.cache/huggingface/hub')
MODEL_DIRNAME = 'models--hfl--chinese-bert-wwm-ext'


def find_in_cache():
    """Search HF cache for the tokenizer files you already downloaded during training."""
    model_dir = os.path.join(CACHE_BASE, MODEL_DIRNAME)
    if not os.path.isdir(model_dir):
        return None

    snapshots_dir = os.path.join(model_dir, 'snapshots')
    if not os.path.isdir(snapshots_dir):
        return None

    snapshot_dirs = sorted([
        d for d in os.listdir(snapshots_dir)
        if os.path.isdir(os.path.join(snapshots_dir, d))
    ], reverse=True)

    for snap in snapshot_dirs:
        snap_path = os.path.join(snapshots_dir, snap)
        if all(os.path.isfile(os.path.join(snap_path, f)) for f in FILES):
            return snap_path
    return None


def main():
    os.makedirs(TOKENIZER_DIR, exist_ok=True)

    if all(os.path.isfile(os.path.join(TOKENIZER_DIR, f)) for f in FILES):
        print('All tokenizer files already in local directory. Nothing to do.')
        return

    cache_path = find_in_cache()
    if cache_path:
        print(f'Found tokenizer files in HF cache: {cache_path}')
        for f in FILES:
            src = os.path.join(cache_path, f)
            dst = os.path.join(TOKENIZER_DIR, f)
            shutil.copy2(src, dst)
            print(f'  [OK] Copied {f}')
        print()
        print('All files copied successfully! System can now run fully offline.')
        return

    print('Could not find tokenizer files in HF cache.')
    print()
    print('You need these 3 small files. Since your network blocks all mirrors,')
    print('please download them manually from any device that CAN access:')
    print()
    print('  https://huggingface.co/hfl/chinese-bert-wwm-ext/tree/main')
    print()
    print('Download these files and place in:')
    print(f'  {TOKENIZER_DIR}')
    print()
    for f in FILES:
        print(f'  - {f}')
    print()
    print('Total: ~110 KB of text files. Takes 10 seconds manually.')
    sys.exit(1)


if __name__ == '__main__':
    main()
