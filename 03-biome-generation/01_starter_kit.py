import sys
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

TILE_WIDTH = 64
TILE_HEIGHT = 32
GRID_SIZE = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()


def screen_to_grid():
    pass


def grid_to_iso():
    pass


def draw_tile_iso():
    pass


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()
