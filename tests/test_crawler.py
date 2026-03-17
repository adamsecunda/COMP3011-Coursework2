import unittest
from unittest.mock import patch, MagicMock
from src.crawler import Crawler

class TestCrawler(unittest.TestCase):
    """
    Unit tests for the Crawler class using mocked HTTP responses.
    """

    def setUp(self):
        """
        Initialise a crawler instance with a 0s delay so tests complete fast.
        """
        self.start_url = "https://example.com"
        self.crawler = Crawler(self.start_url, politeness_delay=0.0)

    @patch('src.crawler.requests.get')
    def test_crawl_extracts_text(self, mock_get):
        """
        Test that the crawler correctly extracts text and stops at max_pages.
        
        Args:
            mock_get: Mocked requests.get method.
        """
        # Mocking a successful HTML response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "text/html"}
        mock_response.text = "<html><body><p>Hello World</p></body></html>"
        mock_get.return_value = mock_response

        # Run crawl for exactly 1 page
        results = self.crawler.crawl(max_pages=1)

        self.assertEqual(len(results), 1)
        self.assertIn(self.start_url, results)
        self.assertEqual(results[self.start_url], "hello world")

    @patch('src.crawler.requests.get')
    def test_crawl_follows_links(self, mock_get):
        """
        Test that the crawler discovers same domain links but ignores others.
        
        Args:
            mock_get: Mocked requests.get method.
        """
        mock_response1 = MagicMock(status_code=200)
        mock_response1.headers = {"content-type": "text/html"}
        mock_response1.text = """
            <a href="/internal">Internal</a>
            <a href="https://other.com/external">External</a>
        """

        mock_response2 = MagicMock(status_code=200)
        mock_response2.headers = {"content-type": "text/html"}
        mock_response2.text = "Internal Page Content"

        mock_get.side_effect = [mock_response1, mock_response2]

        results = self.crawler.crawl(max_pages=5)

        # Should find the start page and the internal link, but not the external one
        self.assertEqual(len(results), 2)
        self.assertIn("https://example.com/internal", results)
        self.assertNotIn("https://other.com/external", results)

    def test_respectful_request_delay(self):
        """
        Test that the politeness delay logic correctly identifies wait time.
        """
        self.crawler.politeness_delay = 10.0
        self.crawler.last_request_time = 0.0
        
        with patch('src.crawler.time.time', return_value=5.0):
            wait = self.crawler.politeness_delay - (5.0 - self.crawler.last_request_time)
            self.assertEqual(wait, 5.0)

if __name__ == "__main__":
    unittest.main()