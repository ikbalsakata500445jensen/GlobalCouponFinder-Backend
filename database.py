from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import settings
from typing import Generator

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def init_db():
    # Use SQLite models for local development
    from models_sqlite import Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
