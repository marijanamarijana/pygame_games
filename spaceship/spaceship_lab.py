import pygame, random, sys
from pygame import *

FPS = 30
WINDOW = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW, WINDOW))
pygame.display.set_caption('Space Scavenger')
font = pygame.font.Font('freesansbold.ttf', 30)

spaceship_img = pygame.image.load("spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (90, 90))

crystal_img = pygame.image.load("energy_crystal.png")
crystal_img = pygame.transform.scale(crystal_img, (40, 40))

asteroid_img = pygame.image.load("asteroid.png")
asteroid_img = pygame.transform.scale(asteroid_img, (60, 60))


def create_spaceship():
    rect = spaceship_img.get_rect(center=(WINDOW // 2, WINDOW - 100))
    return {"rect": rect, "speed": 15}


def create_asteroid(asteroid_size_multiplier=1):
    rect = asteroid_img.get_rect(topleft=(random.randint(0, WINDOW-50), -50))
    width = int(rect.width * asteroid_size_multiplier)
    height = int(rect.height * asteroid_size_multiplier)
    rect.width = width
    rect.height = height
    return {"rect": rect, "speed": 5}


def create_crystal():
    rect = crystal_img.get_rect(topleft=(random.randint(0, WINDOW - 50), -50))
    return {"rect": rect, "speed": 4}


def terminate():
    pygame.quit()
    sys.exit()


def draw_spaceship(spaceship):
    screen.blit(spaceship_img, spaceship)


def update_asteroids(asteroids):
    for asteroid in asteroids[:]:
        asteroid["rect"].y += asteroid["speed"]
        screen.blit(pygame.transform.scale(asteroid_img, (asteroid["rect"].width, asteroid["rect"].height)), asteroid["rect"])
        if asteroid["rect"].top > WINDOW:
            asteroids.remove(asteroid)


def update_crystals_and_get_score(crystals, spaceship, score):
    for crystal in crystals[:]:
        crystal["rect"].y += crystal["speed"]
        screen.blit(crystal_img, crystal["rect"])
        if crystal["rect"].top > WINDOW:
            crystals.remove(crystal)
        if spaceship["rect"].colliderect(crystal["rect"]):
            crystals.remove(crystal)
            score += 1
    return score


def display_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


def game_over(score):
    screen.fill(BLACK)
    text = font.render(f"Game Over! Score: {score}", True, RED)
    screen.blit(text, (WINDOW//2 - text.get_width()//2, WINDOW//2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


def game_won(score):
    screen.fill(BLACK)
    text = font.render(f"You won! Score: {score}", True, BLUE)
    screen.blit(text, (WINDOW//2 - text.get_width()//2, WINDOW//2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


def check_collision(spaceship, asteroids):
    for asteroid in asteroids[:]:
        if spaceship["rect"].colliderect(asteroid["rect"]):
            asteroids.remove(asteroid)
            return True
    return False


def main():
    spaceship = create_spaceship()
    asteroids = []
    crystals = []

    score = 0
    asteroid_timer = 0
    crystal_timer = 0
    asteroid_size_multiplier = 1
    mult_timer = 0

    while True:
        clock.tick(FPS)
        screen.fill(BLACK)

        asteroid_timer += 1
        if asteroid_timer > 30:
            asteroids.append(create_asteroid(asteroid_size_multiplier))
            asteroid_timer = 0

        crystal_timer += 1
        if crystal_timer > 60:
            crystals.append(create_crystal())
            crystal_timer = 0

        draw_spaceship(spaceship['rect'])
        update_asteroids(asteroids)
        score = update_crystals_and_get_score(crystals, spaceship, score)
        display_score(score)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT and spaceship['rect'].x >= 0:
                    spaceship['rect'].x -= spaceship['speed']

                elif event.key == K_RIGHT and spaceship['rect'].x <= WINDOW:
                    spaceship['rect'].x += spaceship['speed']

        if check_collision(spaceship, asteroids):
            game_over(score)

        if score == 100:
            game_won(score)

        mult_timer += 1
        if mult_timer == 350:
            asteroid_size_multiplier += 0.5
            spaceship["speed"] += 2
            mult_timer = 0

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()