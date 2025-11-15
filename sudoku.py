import pygame
import sys
from pygame.locals import *

WINDOW_SIZE = 600
GRID_SIZE = 4
CELL_SIZE = (WINDOW_SIZE - 200) // GRID_SIZE

GRID_PIXEL_SIZE = GRID_SIZE * CELL_SIZE
MARGIN = (WINDOW_SIZE - GRID_PIXEL_SIZE) // 2

FONT_SIZE = 32
BG_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 255)
HIGHLIGHT_COLOR = (200, 200, 200)

ERROR_COLOR = (255, 0, 0)
CELEBRATION_COLOR = (0, 255, 0)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Sudoku solver")
FONT = pygame.font.Font(None, FONT_SIZE)

SUDOKU_GRID = [
    [1, 0, 0, 4],
    [0, 0, 3, 0],
    [0, 4, 0, 0],
    [2, 0, 0, 3]
]


def draw_grid(grid, message, selected=None):
    DISPLAYSURF.fill(BG_COLOR)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):

            rect = pygame.Rect(col * CELL_SIZE + MARGIN, row * CELL_SIZE + MARGIN, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(DISPLAYSURF, GRID_COLOR, rect, 1)

            if (row, col) == selected:
                pygame.draw.rect(DISPLAYSURF, HIGHLIGHT_COLOR, rect)

            num = grid[row][col]
            if num != 0:
                number = FONT.render(str(num), True, TEXT_COLOR)
                DISPLAYSURF.blit(number, number.get_rect(center=rect.center))

    pygame.draw.line(DISPLAYSURF, GRID_COLOR, (MARGIN, WINDOW_SIZE // 2), (WINDOW_SIZE - MARGIN, WINDOW_SIZE // 2), 4)
    pygame.draw.line(DISPLAYSURF, GRID_COLOR, (WINDOW_SIZE // 2, MARGIN), (WINDOW_SIZE // 2, WINDOW_SIZE - MARGIN), 4)

    if message:
        show_invalid_move()

    if is_solved(grid):
        show_solved()


def is_valid_move(grid, row, col, num):
    if num >= 5:
        return False

    if num in grid[row]:
        return False

    if num in [grid[row][col] for row in range(GRID_SIZE)]:
        return False

    if not check_subgrid(grid, row, col, num):
        return False
    return True

 # ne e dobra funkcijava sekogash vrakja invalid move bidejki gi ima site brojki vekje
# def is_solved(grid):
#     for row in range(GRID_SIZE):
#         for col in range(GRID_SIZE):
#             if grid[row][col] == 0 or not is_valid_move(grid, row, col, grid[row][col]):
#                 print("invalid" + str(row) + " " + str(col))
#                 return False
#     return True


def check_subgrid(grid, row, col, num):
    subgrid_size = int(GRID_SIZE ** 0.5)
    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
    for r in range(start_row, start_row + subgrid_size):
        for c in range(start_col, start_col + subgrid_size):
            if grid[r][c] == num:
                return False
    return True


def is_solved(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = grid[row][col]
            if num == 0:
                return False
    return True


def show_invalid_move():
    text = FONT.render("INVALID MOVE", True, ERROR_COLOR)
    DISPLAYSURF.blit(text, text.get_rect(center=(WINDOW_SIZE // 2, MARGIN - 50)))


def show_solved():
    text = FONT.render("YOU SOLVED THE SUDOKU!", True, CELEBRATION_COLOR)
    DISPLAYSURF.blit(text, text.get_rect(center=(WINDOW_SIZE // 2, MARGIN - 50)))


def main():
    message = ""
    message_timer = 0

    grid = [row[:] for row in SUDOKU_GRID]
    selected = None
    while True:

        draw_grid(grid, message, selected)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                #selected = y // CELL_SIZE, x // CELL_SIZE ova e ako cel grid go fakjashe sudokuto

                if MARGIN <= x < MARGIN + GRID_PIXEL_SIZE and MARGIN <= y < MARGIN + GRID_PIXEL_SIZE:
                    col = (x - MARGIN) // CELL_SIZE
                    row = (y - MARGIN) // CELL_SIZE
                    selected = (row, col)

            elif event.type == KEYDOWN and selected:
                row, col = selected
                if event.key == K_BACKSPACE or event.key == K_DELETE:
                    grid[row][col] = 0

                elif K_1 <= event.key <= K_9:
                    num = event.key - K_0
                    if is_valid_move(grid, row, col, num):
                        grid[row][col] = num

                    elif not is_valid_move(grid, row, col, num):
                        message = "INVALID MOVE"
                        message_timer = pygame.time.get_ticks()

                elif event.key == K_RETURN and is_solved(grid):
                    show_solved()

        if message and pygame.time.get_ticks() - message_timer > 1000:
            message = ""

        pygame.display.update()


if __name__ == "__main__":
    main()