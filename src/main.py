import sys
import cmd
from pathlib import Path
from .crawler import Crawler
from .indexer import Indexer
from .search import find_pages

INDEX_PATH = Path("data/index.json")


class SearchShell(cmd.Cmd):
    """
    A CLI for crawling, indexing, and searching.
    """

    intro = "Search Engine CLI. Type help or ? to list commands.\n"
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.indexer: Indexer | None = None

    def do_build(self, arg: str) -> None:
        """
        Runs the crawler, builds the inverted index, and saves it to the
        data directory.
        """
        print("Starting crawl...")
        crawler = Crawler("https://quotes.toscrape.com/", politeness_delay=6.0)
        pages = crawler.crawl(max_pages=100)

        print(f"Crawled {len(pages)} pages. Indexing content...")
        indexer = Indexer()
        indexer.build_from_pages(pages)

        # Ensure the data folder exists before writing to it
        INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        indexer.save(INDEX_PATH)

        self.indexer = indexer
        print(f"Index saved to {INDEX_PATH}")

    def do_load(self, arg: str) -> None:
        """
        Loads a previously saved index from the local JSON file.
        """
        if not INDEX_PATH.exists():
            print("No saved index found. Run 'build' first.")
            return
        self.indexer = Indexer.load(INDEX_PATH)
        print(f"Index loaded with {len(self.indexer.inverted_index)} terms.")

    def do_print(self, arg: str) -> None:
        """
        Displays every URL and word position where a specific term occurs.
        """
        if self.indexer is None:
            print("No index loaded.")
            return

        term = arg.strip().lower()
        if not term:
            print("Usage: print <term>")
            return

        postings = self.indexer.get_postings(term)
        if not postings:
            print(f"'{term}' not found.")
            return

        print(f"'{term}' appears in {len(postings)} documents:")
        for url, positions in sorted(postings.items()):
            # Truncate the position list to keep the terminal output readable
            pos_snippet = f"{positions[:8]}{'...' if len(positions) > 8 else ''}"
            print(f"  {url} -> {len(positions)} times at: {pos_snippet}")

    def do_find(self, arg: str) -> None:
        """
        Searches the index for the subset of documents containing all
        specified terms.
        """
        if self.indexer is None:
            print("No index loaded.")
            return

        if not arg.strip():
            print("Usage: find <term1> <term2> ...")
            return

        urls = find_pages(self.indexer, arg)
        if not urls:
            print("No documents match that combination.")
            return

        print(f"Found {len(urls)} matching documents:")
        for url in urls:
            print(f"  {url}")

    def do_exit(self, arg: str) -> bool:
        """
        Shuts down the search engine interface.
        """
        print("Goodbye.")
        return True

    do_quit = do_exit


if __name__ == "__main__":
    shell = SearchShell()

    # Process optional startup commands
    if len(sys.argv) > 1:
        cmd_arg = sys.argv[1].lower()
        if cmd_arg == "build":
            shell.do_build("")
        elif cmd_arg == "load":
            shell.do_load("")

    shell.cmdloop()
