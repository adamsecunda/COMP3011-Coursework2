from typing import Dict, List, DefaultDict
from collections import defaultdict
import json
import re


class Indexer:
    """
    An inverted index that maps terms to document URLs and their word positions.

    Attributes:
        inverted_index: A nested dictionary structure where the primary key is a
            search term, the secondary key is a URL, and the value is a list of
            integer indices representing word positions.
    """

    def __init__(self):
        """
        Initializes an empty Indexer with a nested defaultdict structure.
        """

        self.inverted_index: DefaultDict[str, DefaultDict[str, List[int]]] = (
            defaultdict(lambda: defaultdict(list))
        )

    def build_from_pages(self, pages: Dict[str, str]) -> None:
        """
        Parses page content to populate the inverted index.

        Identifies individual words using regex and records their specific
        numerical positions within each document.

        Args:
            pages: A dictionary mapping document URLs to their full text strings.
        """
        for url, text in pages.items():
            # Find all words while ignoring punctuation
            words = re.findall(r"\b\w+\b", text)
            for pos, word in enumerate(words):
                if word:
                    # Lowercase here so the search lookup always matches
                    clean_word = word.lower()
                    # Store exactly where this word showed up in the current page
                    self.inverted_index[clean_word][url].append(pos)

    def get_postings(self, term: str) -> Dict[str, List[int]]:
        """
        Retrieves the document mapping and word positions for a specific term.

        Args:
            term: The search term to look up. This is case-insensitive.

        Returns:
            Dict[str, List[int]]: A dictionary where keys are URLs and values
                are lists of word positions. Returns empty if not found.
        """
        return dict(self.inverted_index.get(term.lower(), {}))

    def save(self, filepath: str) -> None:
        """
        Serializes the current index state to a JSON file.

        Args:
            filepath: The system path where the JSON index should be saved.
        """
        # We convert to standard dicts because JSON can't save defaultdicts directly
        data = {term: dict(urls) for term, urls in self.inverted_index.items()}
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    @classmethod
    def load(cls, filepath: str) -> "Indexer":
        """
        Loads a previously saved index from a JSON file.

        Args:
            filepath: The path to the JSON file to be loaded.

        Returns:
            Indexer: A new Indexer instance populated with the data from the file.
                Returns an empty Indexer if the file is missing or corrupted.
        """
        idx = cls()
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Move the raw JSON data back into our flexible defaultdict structure
            for term, postings in data.items():
                for url, pos_list in postings.items():
                    idx.inverted_index[term][url] = pos_list
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return idx
