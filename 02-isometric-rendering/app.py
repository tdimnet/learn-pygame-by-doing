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


def draw_tite_topdown(
    surface: pygame.Surface,
    gx: int,
    gy: int,
    color: tuple[int, int, int]
) -> None:
    x = gx * TITLE_SIZE + 200 # offset to center the grid
    y = gy * TITLE_SIZE + 100

    rect = pygame.Rect(x, y, TITLE_SIZE, TITLE_SIZE)
    pygame.draw.rect(surface, color, rect) # Draw the title
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        rect,
        1
    ) # Draw the border around the tile


def get_tile_at_mouse() -> None:
    pass


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill((30, 30, 30))

    for gx in range(GRID_SIZE):
        for gy in range(GRID_SIZE):
            draw_tite_topdown(screen, gx, gy, (100, 150, 100))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()