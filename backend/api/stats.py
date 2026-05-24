from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models.database import get_db, HistoryRecord

router = APIRouter(prefix="/api/stats", tags=["统计"])


@router.get("/overview")
async def get_overview(db: Session = Depends(get_db)):
    total = db.query(HistoryRecord).count()
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

    today_count = db.query(HistoryRecord).filter(
        HistoryRecord.created_at >= today_start
    ).count()

    avg_positive = db.query(func.avg(HistoryRecord.positive_count)).scalar() or 0
    avg_negative = db.query(func.avg(HistoryRecord.negative_count)).scalar() or 0
    avg_neutral = db.query(func.avg(HistoryRecord.neutral_count)).scalar() or 0
    avg_not = db.query(func.avg(HistoryRecord.not_mentioned_count)).scalar() or 0

    return {
        'total_count': total,
        'today_count': today_count,
        'avg_positive': round(avg_positive, 1),
        'avg_negative': round(avg_negative, 1),
        'avg_neutral': round(avg_neutral, 1),
        'avg_not_mentioned': round(avg_not, 1),
    }


@router.get("/sentiment-distribution")
async def get_sentiment_distribution(db: Session = Depends(get_db)):
    total_positive = db.query(func.sum(HistoryRecord.positive_count)).scalar() or 0
    total_negative = db.query(func.sum(HistoryRecord.negative_count)).scalar() or 0
    total_neutral = db.query(func.sum(HistoryRecord.neutral_count)).scalar() or 0
    total_not = db.query(func.sum(HistoryRecord.not_mentioned_count)).scalar() or 0

    return {
        'labels': ['正面', '中性', '负面', '未提及'],
        'values': [total_positive, total_neutral, total_negative, total_not],
    }


@router.get("/trend")
async def get_trend(days: int = Query(7, ge=1, le=30), db: Session = Depends(get_db)):
    end = datetime.now(timezone.utc).replace(tzinfo=None)
    start = end - timedelta(days=days)

    records = db.query(HistoryRecord).filter(
        HistoryRecord.created_at >= start,
        HistoryRecord.created_at <= end,
    ).order_by(HistoryRecord.created_at.asc()).all()

    daily = {}
    current = start.replace(hour=0, minute=0, second=0, microsecond=0)
    while current <= end:
        key = current.strftime('%m-%d')
        daily[key] = {'date': key, 'count': 0, 'avg_positive': 0, 'avg_negative': 0}
        current += timedelta(days=1)

    for r in records:
        key = r.created_at.strftime('%m-%d')
        if key in daily:
            daily[key]['count'] += 1
            daily[key]['avg_positive'] += r.positive_count
            daily[key]['avg_negative'] += r.negative_count

    for k in daily:
        if daily[k]['count'] > 0:
            daily[k]['avg_positive'] = round(daily[k]['avg_positive'] / daily[k]['count'], 1)
            daily[k]['avg_negative'] = round(daily[k]['avg_negative'] / daily[k]['count'], 1)

    return {'trend': list(daily.values())}
