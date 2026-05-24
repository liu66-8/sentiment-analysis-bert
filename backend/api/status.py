import torch

from fastapi import APIRouter

from backend.settings import bert_model_name, num_labels, num_classes, device
from backend.services.predictor import LABEL_CATEGORIES, LABEL_DISPLAY_NAMES

router = APIRouter(prefix="/api", tags=["系统"])


@router.get("/status")
async def system_status():
    gpu_name = ""
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)

    return {
        'model_name': bert_model_name,
        'device': str(device),
        'gpu_name': gpu_name,
        'model_loaded': True,
        'num_labels': num_labels,
        'num_classes': num_classes,
    }


@router.get("/labels")
async def get_labels():
    labels = []
    for key, display_name in LABEL_DISPLAY_NAMES.items():
        labels.append({
            'key': key,
            'display_name': display_name,
            'category': LABEL_CATEGORIES.get(key, '其他'),
        })
    return {'labels': labels}
