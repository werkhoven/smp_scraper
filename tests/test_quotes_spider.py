import requests
from scrapy.http import HtmlResponse
from tutorial.spiders.quotes_spider import QuotesSpider


class TestQuotesSpider:
    """Integration tests for the QuotesSpider."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.spider = QuotesSpider()

    def test_spider_integration_with_real_website(self):
        """Integration test that makes actual HTTP requests to quotes.toscrape.com."""

        # Make an actual HTTP request to the website
        url = "https://quotes.toscrape.com/page/1/"
        response = requests.get(url, timeout=10)

        # Verify we got a successful response
        assert response.status_code == 200, f"Failed to fetch {url}, status: {response.status_code}"

        # Create a Scrapy response object from the real HTML
        scrapy_response = HtmlResponse(
            url=url,
            body=response.content,
            encoding='utf-8'
        )

        # Parse the response using our spider
        results = list(self.spider.parse(scrapy_response))

        # Verify we got results
        assert len(results) > 0, "No quotes were parsed from the real website"

        # Test the structure and content of scraped items
        for item in results:
            # Verify required fields exist
            assert 'text' in item, f"Missing 'text' field in item: {item}"
            assert 'author' in item, f"Missing 'author' field in item: {item}"
            assert 'tags' in item, f"Missing 'tags' field in item: {item}"

            # Verify data types
            assert isinstance(
                item['text'], str), f"'text' should be string, got: {type(item['text'])}"
            assert isinstance(
                item['author'], str), f"'author' should be string, got: {type(item['author'])}"
            assert isinstance(
                item['tags'], list), f"'tags' should be list, got: {type(item['tags'])}"

            # Verify content quality
            assert len(item['text']) > 0, "Quote text should not be empty"
            assert len(item['author']) > 0, "Author should not be empty"
            assert len(item['tags']) > 0, "Tags should not be empty"

            # Verify quote text format
            assert item['text'].startswith(
                '"'), f"Quote should start with quote mark: {item['text']}"
            assert item['text'].endswith(
                '"'), f"Quote should end with quote mark: {item['text']}"

            # Verify tags are non-empty strings
            for tag in item['tags']:
                assert isinstance(
                    tag, str), f"Tag should be string, got: {type(tag)}"
                assert len(tag) > 0, "Tag should not be empty"

        print(f"Successfully parsed {len(results)} quotes from {url}")

        # Test that we got some expected authors (these are likely to be on the first page)
        authors = [item['author'] for item in results]
        assert 'Albert Einstein' in authors, "Expected to find Albert Einstein quotes"

        # Test that we got some expected tags
        all_tags = []
        for item in results:
            all_tags.extend(item['tags'])
        assert 'inspirational' in all_tags or 'life' in all_tags, "Expected to find common tags"
