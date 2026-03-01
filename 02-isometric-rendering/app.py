import sys
import pygame


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE_SIZE = 40
GRID_SIZE= 10


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()


def draw_tite_topdown() -> None:
    pass


def get_tile_at_mouse() -> None:
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