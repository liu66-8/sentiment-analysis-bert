import asyncio
import json
import uuid
from datetime import datetime, timezone
from io import BytesIO

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from backend.settings import MAX_BATCH_SIZE, MAX_FILE_SIZE_MB
from backend.models.database import get_db, HistoryRecord
from backend.schemas import AnalyzeRequest, AnalyzeResponse, BatchTaskResponse
from backend.services.predictor import predictor

import pandas as pd

router = APIRouter(prefix="/api/analyze", tags=["分析"])

batch_tasks = {}


@router.post("", response_model=AnalyzeResponse)
async def analyze_single(req: AnalyzeRequest, db: Session = Depends(get_db)):
    result, summary, suggestions = await asyncio.to_thread(predictor.predict_one, req.text)

    record = HistoryRecord(
        content=req.text,
        result_json=json.dumps(result, ensure_ascii=False),
        positive_count=summary.get('正面', 0),
        negative_count=summary.get('负面', 0),
        neutral_count=summary.get('中性', 0),
        not_mentioned_count=summary.get('未提及', 0),
    )
    db.add(record)
    db.commit()

    return AnalyzeResponse(content=req.text, predictions=result, summary=summary, suggestions=suggestions)


@router.post("/batch")
async def analyze_batch(
    file: UploadFile = File(...),
    content_col: str = Form("content"),
):
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="仅支持 CSV 文件格式")

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"文件大小不能超过 {MAX_FILE_SIZE_MB}MB")

    df = None
    for encoding in ['utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'gb2312', 'latin-1']:
        try:
            df = pd.read_csv(BytesIO(contents), encoding=encoding)
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception:
            continue
    if df is None:
        raise HTTPException(status_code=400, detail="CSV 解析失败: 文件编码不兼容，请保存为 UTF-8 编码")

    if content_col not in df.columns:
        raise HTTPException(status_code=400, detail=f"CSV 中不存在列 '{content_col}'，可用列: {list(df.columns)}")

    if len(df) > MAX_BATCH_SIZE:
        raise HTTPException(status_code=400, detail=f"单次最多分析 {MAX_BATCH_SIZE} 条数据")

    task_id = str(uuid.uuid4())[:8]
    batch_tasks[task_id] = {
        'status': 'processing',
        'total': len(df),
        'processed': 0,
        'results': [],
        'created_at': datetime.now(timezone.utc).isoformat(),
    }

    results = await asyncio.to_thread(_process_batch, df, content_col, task_id)

    batch_tasks[task_id]['status'] = 'completed'
    batch_tasks[task_id]['results'] = results

    return {
        'task_id': task_id,
        'status': 'completed',
        'total': len(df),
        'processed': len(df),
        'results': results,
    }


def _safe_convert(value):
    import numpy as np
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def _process_batch(df, content_col, task_id):
    results = []
    for idx, row in df.iterrows():
        text = str(row[content_col])
        row_dict = {k: _safe_convert(v) for k, v in row.to_dict().items()}
        row_dict['content'] = text
        try:
            result, summary, suggestions = predictor.predict_one(text)
            row_dict['_predictions'] = result
            row_dict['_summary'] = summary
            row_dict['_suggestions'] = suggestions
        except Exception as e:
            row_dict['_predictions'] = {}
            row_dict['_summary'] = {'正面': 0, '中性': 0, '负面': 0, '未提及': 0}
            row_dict['_suggestions'] = None
            row_dict['_error'] = str(e)
        results.append(row_dict)
        batch_tasks[task_id]['processed'] = idx + 1
    return results


@router.get("/batch/{task_id}")
async def get_batch_result(task_id: str):
    task = batch_tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="任务不存在")

    return {
        'task_id': task_id,
        'status': task['status'],
        'total': task['total'],
        'processed': task['processed'],
        'results': task.get('results', []),
    }
