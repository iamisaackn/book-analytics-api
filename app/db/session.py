# SQLite engine + session factory
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# SQLite for local/demo — swap DATABASE_URL env var for MySQL/PostgreSQL in production
engine = create_engine(
    settings.DATABASE_URL,
    # SQLite needs this for multi-threaded use (FastAPI runs async workers)
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()