# game.py
import pygame
import sys
from trie import Trie, TrieNode
from grid import load_grid

CELL_SIZE = 120
GRID_SIZE = 3
WIDTH = HEIGHT = CELL_SIZE * GRID_SIZE

BG = (240, 240, 240)
GRID_COLOR = (0, 0, 0)
PATH_COLOR = (30, 30, 30)
HIGHLIGHT = (255, 210, 210)

pygame.init()
FONT = pygame.font.SysFont("arial", 48)
SMALL = pygame.font.SysFont("arial", 32)


def load_dictionary(path="dictionary.txt"):
    trie = Trie()
    with open(path, "r") as f:
        for line in f:
            word = line.strip().lower()
            if word:
                trie.insert(word)
    return trie


def get_cell_from_pos(pos):
    x, y = pos
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        return row, col
    return None


def draw_grid(screen, grid, path):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):

            x = c * CELL_SIZE
            y = r * CELL_SIZE

            # Highlight path cells
            if (r, c) in path:
                pygame.draw.rect(screen, HIGHLIGHT, (x, y, CELL_SIZE, CELL_SIZE))

            pygame.draw.rect(screen, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 2)

            # Draw letter
            ch = grid[r][c].upper()
            text = FONT.render(ch, True, (0,0,0))
            screen.blit(text, (x + 40, y + 30))


def draw_path_lines(screen, path):
    if len(path) < 2:
        return

    points = [
        (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2)
        for (r, c) in path
    ]
    pygame.draw.lines(screen, PATH_COLOR, False, points, 8)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 80))
    pygame.display.set_caption("WordTrace (pygame prototype)")

    grid = load_grid()
    trie = load_dictionary()

    dragging = False
    path = []
    current_word = ""

    feedback = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # start tracing
            if event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                path = []
                current_word = ""
                feedback = ""

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

                # check if traced word is valid
                node = trie.has_prefix(current_word)
                if current_word and node and node.is_word:
                    feedback = f"{current_word.upper()} ✔ VALID"
                else:
                    feedback = f"{current_word.upper()} ✘ INVALID"

            # during drag
            if event.type == pygame.MOUSEMOTION and dragging:
                cell = get_cell_from_pos(event.pos)
                if cell and (cell not in path):
                    # ensure adjacency
                    if not path:
                        path.append(cell)
                        current_word += grid[cell[0]][cell[1]]
                    else:
                        pr, pc = path[-1]
                        r, c = cell
                        if abs(pr - r) + abs(pc - c) == 1:  # 4-way adjacency
                            ch = grid[r][c]
                            # prune early if prefix impossible
                            if trie.has_prefix(current_word + ch):
                                path.append(cell)
                                current_word += ch

        # DRAW
        screen.fill(BG)

        draw_grid(screen, grid, path)
        draw_path_lines(screen, path)

        # Draw current word
        wtxt = SMALL.render(current_word.upper(), True, (0, 0, 0))
        screen.blit(wtxt, (10, HEIGHT + 10))

        # Feedback after release
        ftxt = SMALL.render(feedback, True, (0, 120, 0) if "VALID" in feedback else (180, 0, 0))
        screen.blit(ftxt, (10, HEIGHT + 40))

        pygame.display.flip()


if __name__ == "__main__":
    main()
