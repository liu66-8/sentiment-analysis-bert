from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Text, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def _localtime():
    return datetime.now()


class HistoryRecord(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    result_json = Column(Text, nullable=False)
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    not_mentioned_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=_localtime)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'positive_count': self.positive_count,
            'negative_count': self.negative_count,
            'neutral_count': self.neutral_count,
            'not_mentioned_count': self.not_mentioned_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
