# Define here the models for your scraped items

from dataclasses import dataclass, field
import scrapy


@dataclass
class Quote(scrapy.Item):
    text: str | None = field(default=None)
    author: str | None = field(default=None)
    tags: list[str] | None = field(default=None)
