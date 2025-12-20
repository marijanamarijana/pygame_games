import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

font20 = pygame.font.Font('freesansbold.ttf', 20)
clock = pygame.time.Clock()
FPS = 30


def create_striker(x, y, width=10, height=100, speed=8, color=GREEN):
    return {"x": x, "y": y, "w": width, "h": height, "speed": speed, "color": color}


def create_ball(x, y, radius=8, speed=6):
    return {
        "x": x,
        "y": y,
        "r": radius,
        "speed": speed,
        "xFac": 1,
        "yFac": random.choice([-1, 1]),
        "inPlay": True
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
    ball["x"] += ball["speed"] * ball["xFac"]
    ball["y"] += ball["speed"] * ball["yFac"]

    if ball["y"] <= 0 or ball["y"] >= HEIGHT:
        ball["yFac"] *= -1

    if ball["x"] >= WIDTH:
        ball["xFac"] *= -1

    if ball["x"] <= 0:
        ball["inPlay"] = False


def ball_hit_paddle(ball):
    ball["xFac"] *= -1
    ball["speed"] += 0.5
    ball["yFac"] = random.choice([-2, -1, 1, 2])


def draw_striker(striker):
    pygame.draw.rect(screen, striker["color"], striker_rect(striker))


def draw_ball(ball):
    pygame.draw.circle(screen, WHITE, (ball["x"], ball["y"]), ball["r"])


def draw_text(text, x, y, color=WHITE):
    img = font20.render(text, True, color)
    screen.blit(img, (x, y))


def main():

    while True:

        striker = create_striker(20, HEIGHT // 2 - 50)
        ball = create_ball(WIDTH // 2, HEIGHT // 2)

        direction = 0
        score = 0
        paused = False
        running = True

        while running:

            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_p:
                        paused = not paused

                    if not paused:
                        if event.key == pygame.K_UP:
                            direction = -1
                        if event.key == pygame.K_DOWN:
                            direction = 1

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        direction = 0

            if paused:
                draw_text("GAME PAUSED - Press P to resume", 250, 250)
                pygame.display.update()
                clock.tick(FPS)
                continue

            striker_update(striker, direction)
            ball_update(ball)

            if ball_rect(ball).colliderect(striker_rect(striker)):
                ball_hit_paddle(ball)
                score += 1

            if not ball["inPlay"]:
                show_game_over(score)
                running = False
                break

            draw_striker(striker)
            draw_ball(ball)
            draw_text(f"Score: {score}", 20, 20, WHITE)

            pygame.display.update()
            clock.tick(FPS)


def show_game_over(score):
    screen.fill(BLACK)
    draw_text(f"GAME OVER! Final Score: {score}", 300, 250)
    draw_text("Press SPACE to play again", 320, 300)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


if __name__ == "__main__":
    main()
    pygame.quit()
