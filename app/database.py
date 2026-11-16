import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Строка подключения берётся из переменной окружения —
# в Docker её задаёт compose.yaml, локально можно задать руками.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://app:app@localhost:5432/app",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI-зависимость: открывает сессию на время запроса и закрывает после."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
