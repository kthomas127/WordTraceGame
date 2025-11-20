from trie import Trie
from grid import grid as GRID
from solver import find_all_words

def load_dictionary(path="WordTraceGame/dictionary.txt"):
    trie = Trie()
    with open(path, "r") as f:
        for line in f:
            word = line.strip().lower()
        if word:
            trie.insert(word)
    return trie

def print_results(results):
    for word, path in results:
        print(f"{word:10} path: {path}")

def main():
    grid = GRID
    trie = load_dictionary()
    results = find_all_words(grid, trie)
    print("\nFound words:")
    print("-" * 30)
    print_results(results)

if __name__ == "__main__":
    main()