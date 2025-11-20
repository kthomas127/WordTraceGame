from typing import List
from trie import *
from grid import grid

def find_all_words(board: List[List[str]], trie: Trie) -> List[str]:
    rows, columns = len(grid), len(grid[0])
    found = set()

    def dfs(r, c, node, prefix, path):
        char = grid[r][c]
        if char not in node.children:
            return
        node = node.children[char]
        prefix += char
        path.append((r, c))

        if node.is_word:
            found.add((prefix, tuple(path)))

        # check adjacent values
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < columns and (nr, nc) not in path):
                dfs(nr, nc, node, prefix, path)
        path.pop()
    
    for r in range(rows):
        for c in range(columns):
            dfs(r, c, trie.root, "", [])

    return sorted(found)