from sqlalchemy.orm import Session
from src.database.models.naver_news import NaverNews
from datetime import datetime

# -------------------------
# naver_news_crud.py
# 수집 데이터 저장, 조회, 수정, 삭제 처리
# -------------------------


def save_article(db, article):
    """
    뉴스 기사 정보를 DB에 저장
    :param db: db 세션
    :param article: {'title': ..., 'content': ..., 'pub_date': ..., 'press': ..., 'link': ..., 'created_at': ...}
    """

    db_article = NaverNews(
        title=article.get("title"),
        content=article.get("content"),
        pub_date=article.get("pub_date"),
        press=article.get("press"),
        link=article.get("link"),
        created_at=datetime.utcnow()
    )

    try:
        db.add(db_article)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[DB Error] 기사 저장 실패: {e}")


def save_articles_bulk(db, articles):
    """
    여러개의 뉴스 기사를 한 번에 저장
    :param db: db 세션
    :param articles: [{...}, {...}, {...}]
    """
    try:
        db.bulk_insert_mappings(NaverNews, articles)
        db.commit()
        print(f"[INFO] {len(articles)}개의 기사를 수집해 DB에 저장 했습니다.")
    except Exception as e:
        db.rollback()
        print(f"[DB Error] bulk insert에 실패했습니다: {e}")


def get_all_articles(db, limit=10):
    """
    모든 수집된 기사 조회
    :param db: db세션
    :param limit: 반환할 기사 수
    :return:
    """
    try:
        articles = db.query(NaverNews).limit(limit).all()
        return articles
    except Exception as e:
        print(f"[DB Error] 모든 기사 조회 실패 - {e}")
        return []





