from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from src.database.database import Base
from datetime import datetime, timedelta, timezone

# -----------------------
# naver_news.py
# 테이블 모델 정의
# -----------------------


class NaverNews(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    pub_date = Column(DateTime)
    press = Column(String(100))
    link = Column(String(1000), unique=True, nullable=False)
    keyword = Column(String(100))
    create_at = Column(DateTime, default=datetime.utcnow())

    __table_args__ = (
        UniqueConstraint('link', name='uq_article_link'),
    )
