# Test Suite Documentation

## File: test_search.py
### Class: TestSearch
> Tests for the search logic using dummy data.

* **test_single_term**: Verify a single term pulls all documents containing it.
* **test_subset_intersection**: Ensure searching for two terms returns only the document where they overlap.
* **test_empty_intersection**: Verify that a search for terms that never co-occur returns nothing.
* **test_missing_term**: Confirm that a term not present in the index kills the entire search.
* **test_normalization**: Check that the search still works if the query is capitalized.

---

## File: test_indexer.py
### Class: TestIndexer
> Tests for the inverted index logic and serialisation.

* **test_build_index_positions**: Check if words are mapped to the correct URLs and positions.
* **test_case_insensitivity**: Verify that get_postings ignores case.
* **test_save_and_load**: Ensure the index can be serialized and recovered perfectly.
* **test_load_nonexistent_file**: Load should return an empty indexer if the file is missing.

---

## File: test_performance.py
### Class: TestPerformance
> Benchmarks for indexing and search retrieval speeds.

* **test_batch_crawl_efficiency**: Measure the overhead of processing 100 internal links (mocked).
* **test_indexing_speed**: Measure time taken to index 100 documents.
* **test_search_latency**: Measure the latency of a TF-IDF search on a populated index.

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