"""
Database configuration and connection management.

This module handles SQLAlchemy database setup, session management,
and table creation for the Todo API.
"""

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todos.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()


class TodoDB(Base):
    """
    SQLAlchemy model for Todo items.

    This represents the database table structure for storing todos.
    """

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(String(1000), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    priority = Column(String(10), default="medium", nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False
    )

def get_db():
    """
    Database session dependency for FastAPI.

    This generator function provides database sessions to API endpoints
    and ensures proper cleanup after each request.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
