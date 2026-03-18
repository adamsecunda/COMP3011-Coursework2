## File: test_indexer.py
### Class: TestIndexer
> Tests for the inverted index logic and serialisation.

* **test_build_index_positions**: Check if words are mapped to the correct URLs and positions.
* **test_case_insensitivity**: Verify that get_postings ignores case.
* **test_save_and_load**: Ensure the index can be serialized and recovered perfectly.
* **test_load_nonexistent_file**: Load should return an empty indexer if the file is missing.

---

## File: test_integration.py
### Class: TestSearchIntegration
> Integration tests for the crawl-to-search pipeline.

* **test_multi_word_query**: Test that searching multiple words returns the correct intersection.
* **test_shared_terms**: Test that a common word returns all documents in that subset.
* **test_no_overlap**: Verify that terms appearing in different documents return nothing.
* **test_punctuation**: Verify that symbols and punctuation don't break the word lookup.
* **test_case**: Ensure the search is indifferent to capital letters.

---

## File: test_crawler.py
### Class: TestCrawler
> Unit tests for the Crawler class using mocked HTTP responses.

* **test_crawl_extracts_text**: Test that the crawler correctly extracts text and stops at max_pages.

Args:
    mock_get: Mocked requests.get method.
* **test_crawl_follows_links**: Test that the crawler discovers same domain links but ignores others.

Args:
    mock_get: Mocked requests.get method.
* **test_respectful_request_delay**: Test that the politeness delay logic correctly identifies wait time.

---