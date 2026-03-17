from typing import List
from .indexer import Indexer


def find_pages(indexer: Indexer, query: str) -> List[str]:
    """
    Find documents that contain all words from the query.

    Identifies the subset of documents that contains every search term
    provided in the query.

    Args:
        indexer: Initialised indexer containing the inverted index.
        query: Space-separated search terms (case-insensitive).

    Returns:
        List[str]: Sorted list of URLs containing every word in the query.
            Returns an empty list if there are no matches or the query is empty.
    """
    # Break the query into individual words and normalise them
    terms = [t.strip().lower() for t in query.split() if t.strip()]
    if not terms:
        return []

    url_sets = []
    for term in terms:
        postings = indexer.get_postings(term)

        # If any word doesn't exist in the index, the resulting subset must be empty
        if not postings:
            return []

        # Convert the document keys into a set to find the common overlap
        url_sets.append(set(postings.keys()))

    # Find the subset of URLs that appear in every term's collection
    common_urls = set.intersection(*url_sets)

    # Sort the results so the list is easy to read
    return sorted(common_urls)
