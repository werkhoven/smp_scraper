"""Database package for web scraper."""

from db.models import Quote
from db.repositories import QuotesRepository

__all__ = ["Quote", "QuotesRepository"]
