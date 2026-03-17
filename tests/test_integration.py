import unittest
from src.indexer import Indexer
from src.search import find_pages

class TestSearchIntegration(unittest.TestCase):
    """
    Integration tests for the crawl-to-search pipeline.
    """

    def setUp(self):
        """
        Prepare a small set of data for the pipeline tests.
        """
        self.indexer = Indexer()
        self.pages = {
            "leia": "Help me, Obi-Wan Kenobi. You're my only hope.",
            "obi_wan": "The Force is what gives a Jedi his power.",
            "yoda": "Beware of the dark side. Anger, fear, aggression; the dark side of the Force are they.",
            "vader": "No. I am your father."
        }
        self.indexer.build_from_pages(self.pages)

    def test_multi_word_query(self):
        """
        Test that searching multiple words returns the correct intersection.
        """
        # Only Obi-Wan's quote has both 'force' and 'jedi'
        self.assertEqual(find_pages(self.indexer, "force jedi"), ["obi_wan"])

    def test_shared_terms(self):
        """
        Test that a common word returns all documents in that subset.
        """
        # 'Force' appears in both Yoda and Obi-Wan's quotes
        results = find_pages(self.indexer, "Force")
        self.assertEqual(results, ["obi_wan", "yoda"])

    def test_no_overlap(self):
        """
        Verify that terms appearing in different documents return nothing.
        """
        # 'Father' is Vader, 'Hope' is Leia. No overlap.
        self.assertEqual(find_pages(self.indexer, "father hope"), [])

    def test_punctuation(self):
        """
        Verify that symbols and punctuation don't break the word lookup.
        """
        # Checks if the regex handles the semicolon in 'aggression;'
        self.assertEqual(find_pages(self.indexer, "aggression"), ["yoda"])

    def test_case(self):
        """
        Ensure the search is indifferent to capital letters.
        """
        self.assertEqual(find_pages(self.indexer, "JEDI"), ["obi_wan"])

if __name__ == "__main__":
    unittest.main()