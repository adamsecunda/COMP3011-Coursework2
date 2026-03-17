# Search Engine Tool (COMP3011)

A web crawler and search tool designed to index and retrieve information from [quotes.toscrape.com](https://quotes.toscrape.com/).

## Project Overview
The purpose of this project is to develop a search tool with the following features: 
* **Crawl:** Systematically fetch pages from the target website while observing a 6-second politeness window.
* **Index:** Create an inverted index that stores word occurrences, including frequency and position.
* **Search:** Allow users to find pages containing specific search terms or phrases through a command-line interface.

## Installation & Setup

### 1. Requirements
This project is implemented in Python and utilises the following libraries:
* **Requests:** For composing HTTP requests.
* **BeautifulSoup4:** For parsing HTML pages.

### 2. Environment Setup
1. Clone the repository to your local machine.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`.

## Usage
The tool features a command-line interface (shell). Launch it by running: `python3 -m src.main`.

### Commands
| Command | Usage | Description |
| :--- | :--- | :--- |
| **build** | `> build` | Instructs the tool to crawl the website, build the index, and save it to the file system. |
| **load** | `> load` | Loads the previously saved index from the file system. |
| **print** | `> print <word>` | Prints the inverted index entries for a particular word. |
| **find** | `> find <query>` | Returns a list of all pages containing the given query term or phrase. |

## Testing
This project includes a test suite to ensure the reliability of the crawling, indexing, and search components.

To run the tests: `python3 -m unittest discover tests`