import math
from typing import List, Dict
from .indexer import Indexer


def find_pages(indexer: Indexer, query: str) -> List[str]:
    """
    Find documents containing all query terms, ranked by TF-IDF score.

    Calculates the relevance of each document based on term frequency 
    and inverse document frequency, returning the most relevant results first.

    Args:
        indexer: Initialised indexer containing the inverted index.
        query: Space-separated search terms (case-insensitive).

    Returns:
        List[str]: URLs containing every word in the query, sorted by 
            relevance (descending) and then alphabetically.
    """
    # Break the query into individual words and normalise them
    terms = [t.strip().lower() for t in query.split() if t.strip()]
    if not terms:
        return []

    # Identify the total number of unique documents across the entire index
    all_urls = set()
    for postings in indexer.inverted_index.values():
        all_urls.update(postings.keys())
    total_docs = len(all_urls)

    url_sets = []
    term_postings = {}
    for term in terms:
        postings = indexer.get_postings(term)

        # If any word doesn't exist in the index, the resulting subset must be empty
        if not postings:
            return []

        term_postings[term] = postings
        # Convert the document keys into a set to find the common overlap
        url_sets.append(set(postings.keys()))

    # Find the subset of URLs that appear in every term's collection
    common_urls = set.intersection(*url_sets)

    # Calculate TF-IDF scores for the documents in our common subset
    scores: Dict[str, float] = {}
    for url in common_urls:
        score = 0.0
        for term in terms:
            # TF: Count how many times the term appears in this specific page
            tf = len(term_postings[term][url])
            
            # IDF: Logarithmic scale of document rarity across the collection
            # We add 1 to the denominator to prevent division by zero errors
            docs_with_term = len(term_postings[term])
            idf = math.log(total_docs / (1 + docs_with_term))
            
            score += tf * idf
        scores[url] = score

    # Sort results by score (highest first), using URL as a tie-breaker
    return sorted(common_urls, key=lambda x: (-scores[x], x))