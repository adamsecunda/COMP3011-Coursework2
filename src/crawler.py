import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Set


class Crawler:
    """
    Crawler that stays within the given domain and enforces a delay.

    Attributes:
        start_url: The URL where crawling begins.
        politeness_delay: Minimum time (seconds) between consecutive HTTP requests.
        visited: Set of URLs already processed.
        to_visit: Queue of URLs still to be crawled.
        last_request_time: Timestamp of the most recent HTTP request.
    """

    def __init__(self, start_url: str, politeness_delay: float = 6.0):
        """
        Initialise the crawler with starting URL and delay.

        Args:
            start_url: The first page to crawl.
            politeness_delay: Seconds to wait between requests.
        """
        self.start_url = start_url
        self.politeness_delay = politeness_delay
        self.visited: Set[str] = set()
        self.to_visit: List[str] = [start_url]
        self.last_request_time: float = 0.0

    def _respectful_request(self, url: str) -> Optional[requests.Response]:
        """
        Send GET request while respecting the politeness delay.

        Args:
            url: The URL to request.

        Returns:
            Optional[requests.Response]: Response object if the request succeeds, 
                None otherwise.
        """
        now = time.time()
        # Calculate how much time has passed since the last fetch to avoid spamming
        wait = self.politeness_delay - (now - self.last_request_time)
        if wait > 0:
            time.sleep(wait)

        # Identify ourselves properly to the web server
        headers = {"User-Agent": "QuoteIndexBot/1.0 (student project)"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            self.last_request_time = time.time()
            return response
        except requests.RequestException:
            return None

    def crawl(self, max_pages: int = 50) -> Dict[str, str]:
        """
        Crawl pages, extract visible text, and follow same domain links.

        Args:
            max_pages: Maximum number of pages to process (safety limit).

        Returns:
            Dict[str, str]: A mapping of each crawled URL to its cleaned, 
                lowercase text content.
        """
        pages: Dict[str, str] = {}
        base_domain = urlparse(self.start_url).netloc

        while self.to_visit and len(pages) < max_pages:
            url = self.to_visit.pop(0)
            if url in self.visited:
                continue
            
            # Progress output
            sys.stdout.write(f"\r[Attempting] {len(pages)}/{max_pages} | URL: {url[:50]:<60}")
            sys.stdout.flush()

            response = self._respectful_request(url)
            
            # Skip failures or non-HTML files (like PDFs or images)
            if not response or response.status_code != 200:
                self.visited.add(url)
                continue
            if "text/html" not in response.headers.get("content-type", "").lower():
                self.visited.add(url)
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            self.visited.add(url)

            # Extract all human readable text
            text = soup.get_text(separator=" ", strip=True).lower()
            pages[url] = text

            for link in soup.find_all("a", href=True):
                href = link["href"].strip()
                if not href:
                    continue
                # Convert relative links (e.g., '/page/2') into full URLs
                next_url = urljoin(url, href)
                parsed = urlparse(next_url)
                
                # Only queue the link if it's on the same site and we haven't seen it yet
                if (parsed.netloc == base_domain and
                        next_url not in self.visited and
                        next_url not in self.to_visit):
                    self.to_visit.append(next_url)

        sys.stdout.write(f"\r[Success] Crawled {len(pages)} pages.{' ' * 60}\n")
        return pages