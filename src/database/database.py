# ------------------------
# database.py
# DB 연결 및 세션 관리
# ------------------------
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("DB 연결 성공:", result.scalar())
    except Exception as e:
        print("DB 연결 실패:", e)


# test_connection()
