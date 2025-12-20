import pygame, sys, random
from pygame import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Scavenger")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

spaceship_img = pygame.image.load("spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (80, 80))

asteroid_img = pygame.image.load("asteroid.png")
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

crystal_img = pygame.image.load("energy_crystal.png")
crystal_img = pygame.transform.scale(crystal_img, (40, 40))


pygame.mixer.music.load("background_music.wav")
pygame.mixer.music.play(-1)

clash_sound = pygame.mixer.Sound("clash_sound.wav")


def create_spaceship():
    rect = spaceship_img.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
    return {"rect": rect, "speed": 15}


def create_asteroid(asteroid_size_multiplier=1.0):
    rect = asteroid_img.get_rect(topleft=(random.randint(0, WINDOW_WIDTH-50), -50))
    width = int(rect.width * asteroid_size_multiplier)
    height = int(rect.height * asteroid_size_multiplier)
    rect.width = width
    rect.height = height
    return {"rect": rect, "speed": 5}


def create_crystal():
    rect = crystal_img.get_rect(topleft=(random.randint(0, WINDOW_WIDTH-50), -50))
    return {"rect": rect, "speed": 4}


def update_asteroids(asteroids):
    for asteroid in asteroids:
        asteroid["rect"].y += asteroid["speed"]
        screen.blit(pygame.transform.scale(asteroid_img, (asteroid["rect"].width, asteroid["rect"].height)), asteroid["rect"])
        if asteroid["rect"].top > WINDOW_HEIGHT:
            asteroids.remove(asteroid)


def update_crystals(crystals, spaceship, score):
    for crystal in crystals[:]:
        crystal["rect"].y += crystal["speed"]
        screen.blit(crystal_img, crystal["rect"])
        if crystal["rect"].top > WINDOW_HEIGHT:
            crystals.remove(crystal)
        if spaceship["rect"].colliderect(crystal["rect"]):
            crystals.remove(crystal)
            score += 1
    return score


def draw_spaceship(spaceship):
    screen.blit(spaceship_img, spaceship["rect"])


def display_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


def game_over(score):
    screen.fill(BLACK)
    text = font.render(f"Game Over! Score: {score}", True, RED)
    screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


def check_collision(spaceship, asteroids):
    for asteroid in asteroids:
        if spaceship["rect"].colliderect(asteroid["rect"]):
            clash_sound.play()
            return True
    return False


def main():
    spaceship = create_spaceship()
    asteroids = []
    crystals = []

    score = 0
    asteroid_timer = 0
    crystal_timer = 0
    difficulty_timer = 0
    asteroid_size_multiplier = 1.0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BLACK)

        score = update_crystals(crystals, spaceship, score)
        draw_spaceship(spaceship)
        display_score(score)

        asteroid_timer += 1
        if asteroid_timer > 30:
            asteroids.append(create_asteroid(asteroid_size_multiplier))
            asteroid_timer = 0

        crystal_timer += 1
        if crystal_timer > 90:
            crystals.append(create_crystal())
            crystal_timer = 0

        update_asteroids(asteroids)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and spaceship['rect'].left > 0:
                    spaceship["rect"].x -= spaceship["speed"]

                elif event.key == pygame.K_RIGHT and spaceship['rect'].right < WINDOW_WIDTH:
                    spaceship["rect"].x += spaceship["speed"]

                elif event.key == pygame.K_UP and spaceship['rect'].top > 0:
                    spaceship["rect"].y -= spaceship["speed"]

                elif event.key == pygame.K_DOWN and spaceship['rect'].bottom < WINDOW_HEIGHT:
                    spaceship["rect"].y += spaceship["speed"]

        if check_collision(spaceship, asteroids):
            game_over(score)

        difficulty_timer += 1
        if difficulty_timer % 30 == 0:
            asteroid_size_multiplier += 0.1
            spaceship["speed"] += 0.3
            print(spaceship["speed"])

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
