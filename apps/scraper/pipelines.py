# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import asyncio

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from scraper.items import Quote
from scraper.spiders.quotes_spider import QuotesSpider
from scraper.dependencies import get_database_session
from db.repositories import QuotesRepository


class QuotesValidationPipeline:
    def process_item(self, item: Quote, spider: QuotesSpider):
        if item.get("text") is None:
            raise DropItem("Missing text in item")
        if item.get("author") is None:
            raise DropItem("Missing author in item")
        if item.get("tags") is None:
            raise DropItem("Missing tags in item")
        return item


class QuotesDatabasePipeline:
    """Pipeline to save quotes to the database."""

    def __init__(self):
        """Initialize the pipeline."""
        self.session = None
        self.quotes_repo = None

    def open_spider(self, spider):
        """Called when the spider is opened."""
        # Create a new event loop for this thread if needed
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Initialize database session and repository
        self.session = loop.run_until_complete(get_database_session())
        self.quotes_repo = QuotesRepository(self.session)

    def close_spider(self, spider):
        """Called when the spider is closed."""
        if self.session:
            # Close the session
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.session.close())

    def process_item(self, item: Quote, spider: QuotesSpider) -> Quote:
        """Process a quote item and save it to the database."""
        adapter = ItemAdapter(item)

        # Extract data from the item
        text = adapter.get("text")
        author = adapter.get("author")
        tags = adapter.get("tags")

        if not all([text, author, tags]):
            raise DropItem(f"Missing required fields in item: {item}")

        # Check for duplicates and save to database
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._save_quote(text, author, tags))
            spider.logger.info(f"Saved quote: {text[:50]}... by {author}")
        except Exception as e:
            spider.logger.error(f"Failed to save quote: {e}")
            raise DropItem(f"Database error: {e}")

        return item

    async def _save_quote(self, text: str, author: str, tags: str):
        """Save a quote to the database with duplicate checking."""
        # Check if quote already exists
        existing_quote = await self.quotes_repo.find_duplicate(text, author)

        if existing_quote:
            # Update tags if they're different
            if existing_quote.tags != tags:
                await self.quotes_repo.update_tags(existing_quote.id, tags)
        else:
            # Create new quote
            await self.quotes_repo.create(text, author, tags)
