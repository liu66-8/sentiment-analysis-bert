import os
import sys
import time
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import save_folder

FULL_CHECKPOINT = os.path.join(save_folder, 'BEST_checkpoint.tar')
LIGHT_CHECKPOINT = os.path.join(save_folder, 'BEST_checkpoint_inference.tar')


def convert():
    t0 = time.time()
    print(f"[1/3] Reading full checkpoint ({FULL_CHECKPOINT})...")
    checkpoint = torch.load(FULL_CHECKPOINT, map_location='cpu', weights_only=True)
    size_mb = os.path.getsize(FULL_CHECKPOINT) / (1024 * 1024)
    print(f"      Size: {size_mb:.0f} MB, time: {time.time()-t0:.1f}s")

    model_sd = checkpoint.get('model_state_dict', checkpoint)
    print(f"[2/3] Extracting model weights only...")

    torch.save({'model_state_dict': model_sd}, LIGHT_CHECKPOINT)
    light_mb = os.path.getsize(LIGHT_CHECKPOINT) / (1024 * 1024)
    print(f"      Saved to: {LIGHT_CHECKPOINT}")
    print(f"      Size: {light_mb:.0f} MB (saved {size_mb - light_mb:.0f} MB)")
    print(f"[3/3] Done in {time.time()-t0:.1f}s")

    print()
    print("You can now delete the original checkpoint if disk space is tight:")
    print(f"  del \"{FULL_CHECKPOINT}\"")
    print("Or keep both - the system will auto-prefer the lighter one.")


if __name__ == '__main__':
    if not os.path.isfile(FULL_CHECKPOINT):
        print(f"[ERROR] {FULL_CHECKPOINT} not found!")
        sys.exit(1)
    convert()
