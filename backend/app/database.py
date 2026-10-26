"""
Database engine and session management supporting SQLite and PostgreSQL.
Serverless-safe: falls back to /tmp/threat_intel.db in read-only Vercel environments.
"""

import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("ai_threat.database")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # On Vercel or serverless environments, the project root filesystem is read-only.
    # Fall back to the temporary writable directory /tmp for demo and runtime storage.
    if os.getenv("VERCEL") == "1" or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        DATABASE_URL = "sqlite:////tmp/threat_intel.db"
    else:
        DATABASE_URL = "sqlite:///./threat_intel.db"

# Normalize postgres:// scheme (commonly emitted by Render, Supabase, Neon, Heroku) to postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

is_sqlite = DATABASE_URL.startswith("sqlite")

engine_kwargs = {}
if is_sqlite:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs["pool_pre_ping"] = True

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """Create all database tables on startup safely."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info(f"Database initialized successfully with URL target: {DATABASE_URL}")
    except Exception as exc:
        logger.error(f"Error creating database tables: {exc}")


def get_db():
    """Dependency injection helper for FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()