import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

font20 = pygame.font.Font('freesansbold.ttf', 20)
clock = pygame.time.Clock()
FPS = 30


def create_striker(x, y):
    return {
        "x": x,
        "y": y,
        "w": 10,
        "h": 100,
        "speed": 8,
    }


def create_ball(x, y):
    return {
    "x": x,
    "y": y,
    "r": 8,
    "speed": 6,
    "x_direction": 1,
    "y_direction": random.choice([-1, 1]),
    "play": True
    }


def striker_rect(striker):
    return pygame.Rect(striker["x"], striker["y"], striker["w"], striker["h"])


def ball_rect(ball):
    return pygame.Rect(ball["x"] - ball["r"], ball["y"] - ball["r"], ball["r"] * 2, ball["r"] * 2)


def striker_update(striker, direction):
    striker["y"] += striker["speed"] * direction

    if striker["y"] < 0:
        striker["y"] = 0
    if striker["y"] + striker["h"] > HEIGHT:
        striker["y"] = HEIGHT - striker["h"]


def ball_update(ball):
    ball["x"] += ball["speed"] * ball["x_direction"]
    ball["y"] += ball["speed"] * ball["y_direction"]

    # top/bottom
    if ball["y"] <= 0 or ball["y"] >= HEIGHT:
        ball["y_direction"] *= -1

    # right
    if ball["x"] >= WIDTH:
        ball["x_direction"] *= -1

    # missed (left side)
    if ball["x"] <= 0:
        ball["play"] = False


def ball_hit_paddle(ball):
    ball["x_direction"] *= -1
    ball["speed"] += 0.5
    ball["y_direction"] = random.choice([-2, -1, 1, 2])


def draw_striker(striker):
    pygame.draw.rect(screen, GREEN, striker_rect(striker))


def draw_ball(ball):
    pygame.draw.circle(screen, WHITE, (ball["x"], ball["y"]), ball["r"])


def draw_text(text, x, y):
    txt = font20.render(text, True, WHITE)
    screen.blit(txt, (x, y))


def main():

    while True:

        striker = create_striker(20, random.randint(10, HEIGHT))
        ball = create_ball(random.randint(10, WIDTH), random.randint(10, HEIGHT))

        direction = 0
        score = 0
        paused = False

        while True:

            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        paused = not paused

                    if not paused:
                        if event.key == pygame.K_UP:
                            direction = -1
                        if event.key == pygame.K_DOWN:
                            direction = 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0

            if paused:
                draw_text("GAME PAUSED - Press SPACE to resume", 250, 250)
                pygame.display.update()
                clock.tick(FPS)
                continue

            striker_update(striker, direction)
            ball_update(ball)

            if ball_rect(ball).colliderect(striker_rect(striker)):
                ball_hit_paddle(ball)
                score += 1

            if not ball["play"]:
                show_game_over(score)
                break

            draw_striker(striker)
            draw_ball(ball)
            draw_text(f"Score: {score}", 20, 20)

            pygame.display.update()
            clock.tick(FPS)


def show_game_over(score):
    screen.fill(BLACK)
    draw_text(f"GAME OVER! Final Score: {score}", 300, 250)
    draw_text("Press SPACE to play again", 310, 300)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    break


if __name__ == "__main__":
    main()