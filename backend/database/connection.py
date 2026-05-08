"""
Module: connection.py
Purpose: SQLAlchemy database engine and session factory for PostgreSQL/Supabase.
"""
import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker  # FIX: declarative_base moved in SQLAlchemy 2.x
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # FIX: Instead of raising at import time (which crashes the Streamlit app),
    # we log a warning and use a SQLite fallback so the app can still start
    # when no DB is configured.
    logger.warning(
        "DATABASE_URL not found in .env — falling back to local SQLite database. "
        "History/analytics features will be local-only."
    )
    DATABASE_URL = "sqlite:///./deaf_connect_local.db"

# Configure the SQLAlchemy engine
# pool_pre_ping=True is essential for Supabase/PostgreSQL to handle idle connection timeouts
if DATABASE_URL.startswith("sqlite"):
    # SQLite doesn't support pool options like pool_size / max_overflow
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False},  # Required for SQLite + FastAPI
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Export engine and SessionLocal for use in other modules
__all__ = ["engine", "SessionLocal", "Base", "get_db"]

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
