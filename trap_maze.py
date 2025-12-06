import pygame, sys
from pygame import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 60
GRID_COLS = 8
GRID_ROWS = 6
STATUS_BAR = 80
FPS = 30

BLACK    = (0,    0,    0)
GRAY     = (150, 150, 150)
WHITE    = (255, 255, 255)
DARKGRAY = (50,  50,   50)
GREEN    = (0,   200,   0)
RED      = (200,   0,   0)
BLUE     = (0,   0,   200)

LEVEL = [
    "........",
    ".T..T..E",
    "....T...",
    ".TT.....",
    ".S......",
    "........"
]


def parse_level():
    traps = set()
    start = exitp = None
    for r, row in enumerate(LEVEL):
        for c,ch in enumerate(row):
            if ch == "S": start = (c,r)
            if ch == "E": exitp = (c,r)
            if ch == "T": traps.add((c,r))
    return start, exitp, traps


def grid_origin():
    w = GRID_COLS * CELL_SIZE
    h = GRID_ROWS * CELL_SIZE
    return (WINDOW_WIDTH-w)//2, STATUS_BAR + (WINDOW_HEIGHT-STATUS_BAR-h)//2


def draw_board(screen, player):
    _, exitp, traps = parse_level()
    screen.fill(BLACK)

    pygame.draw.rect(screen, DARKGRAY, (0, 0, WINDOW_WIDTH, STATUS_BAR))

    gx, gy = grid_origin()
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            rect = pygame.Rect(gx + c * CELL_SIZE, gy + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, DARKGRAY, rect, 1)

            if (c, r) == exitp:
                pygame.draw.rect(screen, BLUE, rect)

            if (c, r) == tuple(player):
                player_rect = pygame.Rect(rect.x + 10, rect.y + 10, CELL_SIZE - 20, CELL_SIZE - 20)
                pygame.draw.rect(screen, GREEN, player_rect)

            if (c, r) in traps and flag:
                player_rect = pygame.Rect(gx + c * CELL_SIZE, gy + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, RED, player_rect)


def can_move(x, y, player):
    last_x, last_y = player

    if x == -1  or y == -1 or x == GRID_COLS or y == GRID_ROWS:
        return False

    if (abs(x - last_x) != 0 and abs(x - last_x) != 1) or (abs(y - last_y) != 0 and abs(y - last_y) != 1):
        return False

    return True


def main():
    global flag

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("Trap Maze")
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 32)

    start, exitp, traps = parse_level()
    player = list(start)
    message = "Memorize traps!"
    reveal_start = pygame.time.get_ticks()
    REVEAL_MS = 2500
    state = "REVEAL"
    lives = 3
    moves = 0

    message_timer = 0
    flag = True

    while True:
        clock.tick(FPS)

        draw_board(screen, player)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()

                if e.key == pygame.K_r:
                    start, exitp, traps = parse_level()
                    player = list(start)
                    lives = 3
                    moves = 0

                if state == "PLAY":
                    x, y = player

                    if e.key == K_DOWN:
                        if can_move(x, y + 1, player):
                            y = y + 1
                            player = [x, y]
                            moves += 1

                    elif e.key == K_UP:
                        if can_move(x, y - 1, player):
                            y = y - 1
                            player = [x, y]
                            moves += 1

                    elif e.key == K_LEFT:
                        if can_move(x - 1, y, player):
                            x = x - 1
                            player = [x, y]
                            moves += 1

                    elif e.key == K_RIGHT:
                        if can_move(x + 1, y, player):
                            x = x + 1
                            player = [x, y]
                            moves += 1

                    if (player[0], player[1]) in traps:
                        lives -= 1
                        player = list(start)
                        if lives == 0:
                            state = "LOST"
                            message_timer = pygame.time.get_ticks()

                    if (player[0], player[1]) == exitp:
                        state = "WON"
                        message_timer = pygame.time.get_ticks()

        if state == "REVEAL":
            if pygame.time.get_ticks() - reveal_start >= REVEAL_MS:
                state = "PLAY"
                message = "Go!"
                flag = False

        if state == "WON":
            message = "YOU WON"

        if state == "LOST":
            message = "YOU LOST"

        if state == "LOST" or state == "WON":
            text = font.render(message, True, RED)
            screen.blit(text, text.get_rect(center=(WINDOW_WIDTH // 2, STATUS_BAR // 2)))

            if pygame.time.get_ticks() - message_timer >= REVEAL_MS:
                sys.exit()

        else:
            text = font.render(message, True, RED)
            screen.blit(text, text.get_rect(center=(WINDOW_WIDTH // 2, STATUS_BAR // 2 - 20)))

            text = font.render(f"Lives: {lives}, Moves = {moves}", True, WHITE)
            screen.blit(text, text.get_rect(center=(WINDOW_WIDTH // 2, STATUS_BAR // 2 + 20)))

        pygame.display.update()


if __name__ == "__main__":
    main()
