from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
    
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_word = True

    def search(self, word: str) -> bool:
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_word
    
    def has_prefix(self, prefix: str) -> bool:
        node = self.root
        for c in prefix:
            if c not in node.children:
                return False
            node = node.children[c]
        return True
    
# testing
ops = [
    ("insert", "top"),
    ("insert", "bye"),
    ("has_prefix", "to"),
    ("search", "to"),
    ("insert", "to"),
    ("search", "to"),
]

trie = Trie()

for op, arg in ops:
    result = getattr(trie, op)(arg)
    if result is not None:
        print(result)