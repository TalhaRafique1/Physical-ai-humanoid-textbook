"""
Database configuration for the textbook generation system.

This module handles database connection configuration for Neon PostgreSQL.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings

# Try to import SQLAlchemy components, but provide fallbacks
try:
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    # Define placeholders to avoid NameError
    create_engine = None
    declarative_base = None
    sessionmaker = None
    SQLALCHEMY_AVAILABLE = False


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/textbook_generation")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        env_file = ".env"


# Initialize settings
settings = DatabaseSettings()


def get_database_url() -> str:
    """Get the database URL from settings or environment."""
    return settings.database_url


# For sync operations (if needed)
if SQLALCHEMY_AVAILABLE:
    sync_engine = create_engine(
        settings.database_url.replace("+asyncpg", ""),  # Use regular postgresql driver
        echo=settings.debug,
    )
else:
    sync_engine = None

# For async operations
if SQLALCHEMY_AVAILABLE:
    try:
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

        async_engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
        )

        async_session_local = sessionmaker(
            async_engine, class_=AsyncSession, expire_on_commit=False
        )
    except ImportError:
        # If async drivers are not available, fall back to sync
        async_engine = None
        async_session_local = None
else:
    # If SQLAlchemy is not available at all
    async_engine = None
    async_session_local = None


def get_db_session():
    """Get a database session."""
    if SQLALCHEMY_AVAILABLE and async_session_local:
        return async_session_local()
    elif SQLALCHEMY_AVAILABLE and sync_engine:
        # Fallback to sync session
        return sessionmaker(bind=sync_engine)()
    else:
        # Return None or raise an exception if DB is required
        return None


if SQLALCHEMY_AVAILABLE:
    Base = declarative_base()
else:
    # Fallback base class if SQLAlchemy is not available
    class Base:
        pass


# Example usage:
# from sqlalchemy import text
# async with async_engine.begin() as conn:
#     await conn.execute(text("SELECT 1"))