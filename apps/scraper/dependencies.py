"""Dependency injection for the scraper application."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from scraper.settings import (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD,
)


def get_database_url() -> str:
    """Get the database URL from settings."""
    return f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


def create_database_engine():
    """Create the database engine."""
    database_url = get_database_url()
    return create_async_engine(
        database_url,
        echo=False,  # Set to True for SQL debugging
        pool_pre_ping=True,  # Verify connections before use
    )


def create_session_factory(engine):
    """Create a session factory."""
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


# Global engine and session factory
_engine = None
_session_factory = None


def get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        _engine = create_database_engine()
    return _engine


def get_session_factory():
    """Get or create the session factory."""
    global _session_factory
    if _session_factory is None:
        engine = get_engine()
        _session_factory = create_session_factory(engine)
    return _session_factory


async def get_database_session() -> AsyncSession:
    """Get a database session."""
    session_factory = get_session_factory()
    return session_factory()
