import json

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from backend.models.database import get_db, HistoryRecord

router = APIRouter(prefix="/api/history", tags=["历史记录"])


@router.get("")
async def list_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(HistoryRecord).count()
    records = (
        db.query(HistoryRecord)
        .order_by(HistoryRecord.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    items = []
    for r in records:
        items.append({
            'id': r.id,
            'content_preview': r.content[:100] + ('...' if len(r.content) > 100 else ''),
            'positive_count': r.positive_count,
            'negative_count': r.negative_count,
            'neutral_count': r.neutral_count,
            'not_mentioned_count': r.not_mentioned_count,
            'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'items': items,
    }


@router.get("/{record_id}")
async def get_history_detail(record_id: int, db: Session = Depends(get_db)):
    record = db.query(HistoryRecord).filter(HistoryRecord.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="记录不存在")

    predictions = json.loads(record.result_json)

    summary = {
        '正面': record.positive_count,
        '中性': record.neutral_count,
        '负面': record.negative_count,
        '未提及': record.not_mentioned_count,
    }

    suggestions = None
    try:
        from backend.services.llm_suggestions import generate_llm_suggestions
        suggestions = generate_llm_suggestions(record.content, predictions, summary)
    except Exception:
        pass

    return {
        'id': record.id,
        'content': record.content,
        'predictions': predictions,
        'suggestions': suggestions,
        'positive_count': record.positive_count,
        'negative_count': record.negative_count,
        'neutral_count': record.neutral_count,
        'not_mentioned_count': record.not_mentioned_count,
        'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }


@router.delete("/{record_id}")
async def delete_history(record_id: int, db: Session = Depends(get_db)):
    record = db.query(HistoryRecord).filter(HistoryRecord.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="记录不存在")

    db.delete(record)
    db.commit()
    return {"message": "删除成功"}
