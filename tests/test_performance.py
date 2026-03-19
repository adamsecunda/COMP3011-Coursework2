import unittest
import time
from src.crawler import Crawler
from src.indexer import Indexer
from src.search import find_pages

class TestPerformance(unittest.TestCase):
    """
    Benchmarks for indexing and search retrieval speeds.
    """

    def setUp(self):
        self.indexer = Indexer()
        # Create a mock dataset
        self.large_data = {f"url_{i}": "word " * 100 for i in range(100)}
        self.start_url = "https://example.com"
        self.crawler = Crawler(self.start_url, politeness_delay=0.0)

    def test_batch_crawl_efficiency(self):
        """
        Measure the overhead of processing 100 internal links (mocked).
        """
        start_time = time.time()
        
        # Simulate seen URL set and queue management for 100 links
        for i in range(100):
            self.crawler.visited.add(f"https://example.com/{i}")
            
        duration = time.time() - start_time
        print(f"\n100 internal link processing overhead: {duration:.6f}s")
    
        # Ensure internal set management is sub-millisecond
        self.assertLess(duration, 0.01)

    def test_indexing_speed(self):
        """
        Measure time taken to index 100 documents.
        """
        start_time = time.time()
        self.indexer.build_from_pages(self.large_data)
        duration = time.time() - start_time
        
        print(f"Indexing 100 docs took: {duration:.4f}s")
        # Ensure it finishes in under 1 second
        self.assertLess(duration, 1.0)

    def test_search_latency(self):
        """
        Measure the latency of a TF-IDF search on a populated index.
        """
        self.indexer.build_from_pages(self.large_data)
        
        start_time = time.time()
        # Run 100 searches to get an average
        for i in range(100):  
            find_pages(self.indexer, "word")
        avg_duration = (time.time() - start_time) / 100
        
        print(f"Average search latency: {avg_duration:.6f}s")
        # Must be faster than 10ms
        self.assertLess(avg_duration, 0.01) 
        