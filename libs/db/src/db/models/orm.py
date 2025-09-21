"""SQLAlchemy ORM models."""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import DeclarativeBase


class BaseEntity(DeclarativeBase):
    """Base entity for all models."""

    pass


class Quote(BaseEntity):
    """Quote model representing a quote from the web scraper."""

    __tablename__ = "quotes"

    id: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    text: str = Column(String, nullable=False)
    author: str = Column(String, nullable=False)
    tags: str = Column(String, nullable=False)
    created_at: datetime = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.now()
    )
    updated_at: datetime = Column(
        TIMESTAMP(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self) -> str:
        """String representation of the Quote model."""
        return f"<Quote(id={self.id}, author='{self.author}', text='{self.text[:50]}...')>"
