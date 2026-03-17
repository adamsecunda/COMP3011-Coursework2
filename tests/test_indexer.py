import unittest
import os
from pathlib import Path
from src.indexer import Indexer


class TestIndexer(unittest.TestCase):
    """
    Tests for the inverted index logic and serialisation.
    """

    def setUp(self):
        """
        Create a fresh indexer and a temporary path for file tests.
        """
        self.indexer = Indexer()
        self.test_file = "tests/temp_index.json"

    def tearDown(self):
        """
        Clean up the temporary file if it was created.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_build_index_positions(self):
        """
        Check if words are mapped to the correct URLs and positions.
        """
        pages = {"url_1": "apple banana apple", "url_2": "banana cherry"}
        self.indexer.build_from_pages(pages)

        # 'apple' appears at index 0 and 2 in url_1
        apple_postings = self.indexer.get_postings("apple")
        self.assertEqual(apple_postings["url_1"], [0, 2])
        self.assertNotIn("url_2", apple_postings)

        # 'banana' appears in both
        banana_postings = self.indexer.get_postings("banana")
        self.assertEqual(banana_postings["url_1"], [1])
        self.assertEqual(banana_postings["url_2"], [0])

    def test_case_insensitivity(self):
        """
        Verify that get_postings ignores case.
        """
        self.indexer.build_from_pages({"url": "Python"})

        # Searching for 'python' should find 'Python'
        self.assertEqual(len(self.indexer.get_postings("python")), 1)
        self.assertEqual(len(self.indexer.get_postings("PYTHON")), 1)

    def test_save_and_load(self):
        """
        Ensure the index can be serialized and recovered perfectly.
        """
        pages = {"url": "data structure"}
        self.indexer.build_from_pages(pages)
        self.indexer.save(self.test_file)

        # Load into a new instance
        new_indexer = Indexer.load(self.test_file)

        # Verify the content survived write to disk
        self.assertEqual(
            new_indexer.get_postings("data"), self.indexer.get_postings("data")
        )
        # Check that the loaded indexer is still a functional defaultdict
        self.assertIn("url", new_indexer.get_postings("data"))

    def test_load_nonexistent_file(self):
        """
        Load should return an empty indexer if the file is missing.
        """
        idx = Indexer.load("not_a_real_file.json")
        self.assertEqual(len(idx.inverted_index), 0)


if __name__ == "__main__":
    unittest.main()
