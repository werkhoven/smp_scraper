"""Quotes repository for database operations."""

import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.orm import Quote


class QuotesRepository:
    """Repository for managing Quote entities."""

    def __init__(self, session: AsyncSession):
        """Initialize the repository with a database session.

        Args:
            session: Async database session
        """
        self.session = session

    async def create(
        self,
        text: str,
        author: str,
        tags: str
    ) -> Quote:
        """Create a new quote.

        Args:
            text: The quote text
            author: The quote author
            tags: The quote tags

        Returns:
            The created Quote instance

        Raises:
            ValueError: If a duplicate quote exists
        """

        quote = Quote(
            text=text,
            author=author,
            tags=tags
        )

        self.session.add(quote)
        await self.session.commit()
        await self.session.refresh(quote)

        return quote

    async def delete(self, quote_id: uuid.UUID) -> bool:
        """Delete a quote by ID.

        Args:
            quote_id: The UUID of the quote to delete

        Returns:
            True if the quote was deleted, False if not found
        """
        result = await self.session.execute(
            delete(Quote).where(Quote.id == quote_id)
        )

        await self.session.commit()

        return result.rowcount > 0

    async def get_by_id(self, quote_id: uuid.UUID) -> Quote | None:
        """Get a quote by ID.

        Args:
            quote_id: The UUID of the quote to retrieve

        Returns:
            The Quote instance if found, None otherwise
        """
        result = await self.session.execute(
            select(Quote).where(Quote.id == quote_id)
        )

        return result.scalar_one_or_none()

    async def find_duplicate(self, text: str, author: str) -> Quote | None:
        """Check if a quote with the same text and author already exists.

        Args:
            text: The quote text to search for
            author: The quote author to search for

        Returns:
            The existing Quote instance if found, None if no duplicate exists
        """
        result = await self.session.execute(
            select(Quote).where(
                Quote.text == text,
                Quote.author == author
            )
        )

        return result.scalar_one_or_none()

    async def update_tags(self, quote_id: uuid.UUID, tags: str) -> Quote:
        """Update the tags of a quote.

        Args:
            quote_id: The UUID of the quote to update
            tags: The new tags for the quote

        Returns:
            The updated Quote instance
        """
        quote = await self.get_by_id(quote_id)
        if quote is None:
            raise ValueError("Quote not found")

        quote.tags = tags
        await self.session.commit()
        await self.session.refresh(quote)

        return quote
