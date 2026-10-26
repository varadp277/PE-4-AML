
"""
Database engine and session management using SQLAlchemy and SQLite.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./threat_intel.db")

is_sqlite = DATABASE_URL.startswith("sqlite")

# On Vercel, use temporary writable storage for SQLite demo data.
if is_sqlite and os.getenv("VERCEL") == "1":
    DATABASE_URL = "sqlite:////tmp/threat_intel.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if is_sqlite else {}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """Dependency injection helper for FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
