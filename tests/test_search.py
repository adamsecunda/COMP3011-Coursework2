import unittest
from src.indexer import Indexer
from src.search import find_pages

class TestSearch(unittest.TestCase):
    """
    Tests for the search logic using dummy data.
    """

    def setUp(self):
        """
        Create a pre-populated indexer with arbitrary strings.
        """
        self.indexer = Indexer()
        # Using meaningless labels to test raw intersection logic
        pages = {
            "doc_a": "aaa bbb ccc",
            "doc_b": "aaa ddd eee",
            "doc_c": "ccc fff ggg"
        }
        self.indexer.build_from_pages(pages)

    def test_single_term(self):
        """
        Verify a single term pulls all documents containing it.
        """
        results = find_pages(self.indexer, "aaa")
        self.assertEqual(results, ["doc_a", "doc_b"])

    def test_subset_intersection(self):
        """
        Ensure searching for two terms returns only the document where they overlap.
        """
        # Only doc_a has both 'aaa' and 'ccc'
        results = find_pages(self.indexer, "aaa ccc")
        self.assertEqual(results, ["doc_a"])

    def test_empty_intersection(self):
        """
        Verify that a search for terms that never co-occur returns nothing.
        """
        # 'bbb' is in doc_a, 'ddd' is in doc_b. No document has both.
        results = find_pages(self.indexer, "bbb ddd")
        self.assertEqual(results, [])

    def test_missing_term(self):
        """
        Confirm that a term not present in the index kills the entire search.
        """
        # 'zzz' does not exist in the indexer
        results = find_pages(self.indexer, "aaa zzz")
        self.assertEqual(results, [])

    def test_normalization(self):
        """
        Check that the search still works if the query is capitalized.
        """
        results = find_pages(self.indexer, "CCC")
        self.assertEqual(results, ["doc_a", "doc_c"])

if __name__ == "__main__":
    unittest.main()