from pathlib import Path

import scrapy
from scrapy.http import Response
from scrapy.loader import ItemLoader

from tutorial.items import Quote


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response: Response):
        for quote in response.css("div.quote"):
            loader = ItemLoader(Quote(), quote)
            loader.add_css("text", "span.text::text")
            loader.add_css("author", "small.author::text")
            loader.add_css("tags", "div.tags a.tag::text")
            yield loader.load_item()

        for a in response.css("ul.pager a"):
            yield response.follow(a, callback=self.parse)
