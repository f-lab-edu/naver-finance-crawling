from src.database.database import engine
from src.database.models import Base


def create_all_tables():
    Base.metadata.create_all(bind=engine)


create_all_tables()