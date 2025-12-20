import pygame, random, sys
from pygame import *

FPS = 60
ROWS = 8
COLS = 8
CELL_SIZE = 80
MARGIN = 100
WIDTH, HEIGHT = COLS * CELL_SIZE + 2 * MARGIN, ROWS * CELL_SIZE + 2 * MARGIN

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# you need to upload your own pictures, they are not provided
# the code won't run without pictures

candy1_img = pygame.image.load("candy1.png")
candy1_img = pygame.transform.scale(candy1_img, (CELL_SIZE, CELL_SIZE))

candy2_img = pygame.image.load("candy2.png")
candy2_img = pygame.transform.scale(candy2_img, (CELL_SIZE, CELL_SIZE))

candy3_img = pygame.image.load("candy3.png")
candy3_img = pygame.transform.scale(candy3_img, (CELL_SIZE, CELL_SIZE))

candy4_img = pygame.image.load("candy4.png")
candy4_img = pygame.transform.scale(candy4_img, (CELL_SIZE, CELL_SIZE))

CANDIES = [candy1_img, candy2_img, candy3_img, candy4_img]

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Candy Crush')
font = pygame.font.Font('freesansbold.ttf', 30)


board = [[random.randint(0, len(CANDIES) - 1) for x in range(COLS)] for y in range(ROWS)]
selected = None
score = 0


def draw_board():
    screen.fill(GREY)
    for r in range(ROWS):
        for c in range(COLS):
            candy = board[r][c]
            if candy is not None:
                screen.blit(CANDIES[candy], (c * CELL_SIZE + MARGIN, r * CELL_SIZE + MARGIN))
                pygame.draw.rect(screen, (60, 60, 60),
                (c * CELL_SIZE + MARGIN, r * CELL_SIZE + MARGIN, CELL_SIZE, CELL_SIZE),2)


def terminate():
    pygame.quit()
    sys.exit()


def draw_text():
    pygame.draw.rect(screen, GREY, (0, HEIGHT - 60, WIDTH, 60))
    txt = font.render(f"Score: {score}", True, WHITE)
    screen.blit(txt, (10, HEIGHT - 45))


def get_cell(pos):
    x, y = pos
    if y < MARGIN or y > HEIGHT - MARGIN:
        return None
    return (y - MARGIN) // CELL_SIZE, (x - MARGIN) // CELL_SIZE


def swap(a, b):
    ar, ac = a
    br, bc = b
    board[ar][ac], board[br][bc] = board[br][bc], board[ar][ac]


def find_matches_for_row(row):
    matches = set()

    for c in range(COLS - 2):
        t = board[row][c]

        if t is None:
            continue

        if t == board[row][c + 1] == board[row][c + 2]:
            matches.add((row, c))
            matches.add((row, c + 1))
            matches.add((row, c + 2))

    return matches


def find_matches_for_col(col):
    matches = set()

    for r in range(ROWS - 2):
        t = board[r][col]

        if t is None:
            continue

        if t == board[r + 1][col] == board[r + 2][col]:
            matches.add((r, col))
            matches.add((r + 1, col))
            matches.add((r + 2, col))

    return matches


def remove_matches(matches, score):
    for r, c in matches:
        board[r][c] = None
        score += 10
    return score


def fill_empty_cells():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] is None:
                board[r][c] = random.randint(0, len(CANDIES) - 1)


def main():
    global selected, score
    while True:
        clock.tick(FPS)

        draw_board()
        draw_text()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                cell = get_cell(event.pos)

                if cell:
                    if selected is None:
                        selected = cell

                    else:
                        if selected != cell:
                            ar, ac = selected
                            br, bc = cell
                            matches1 = set()
                            matches2 = set()
                            matches3 = set()

                            if abs(ar - br) == 1 and ac == bc:
                                swap(selected, cell)
                                matches1 = find_matches_for_col(ac)
                                matches2 = find_matches_for_row(ar)
                                matches3 = find_matches_for_row(br)

                            if abs(ac - bc) == 1 and ar == br:
                                swap(selected, cell)
                                matches1 = find_matches_for_row(ar)
                                matches2 = find_matches_for_col(ac)
                                matches3 = find_matches_for_col(bc)

                            if matches1 or matches2 or matches3:
                                score = remove_matches(matches1, score)
                                score = remove_matches(matches2, score)
                                score = remove_matches(matches3, score)
                                fill_empty_cells()
                            else:
                                swap(selected, cell)
                                selected = None

        pygame.display.update()


if __name__ == '__main__':
    main()