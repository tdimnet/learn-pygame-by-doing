import sys
import pygame


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
GRID_SIZE = 10

TILE_WIDTH = 64
TILE_HEIGHT = 32


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()


def screen_to_grid(
    screen_x: int,
    screen_y: int    
) -> tuple[int, int]:
    x = screen_x- SCREEN_WIDTH // 2
    y = screen_y - 200

    gx = (y / (TILE_HEIGHT / 2) + x / (TILE_WIDTH / 2)) / 2
    gy = (y / (TILE_HEIGHT / 2) - x / (TILE_WIDTH / 2)) / 2

    return int(gx), int(gy)


def grid_to_iso(gx: int, gy: int) -> tuple[int, int]:
    x = (gx - gy) * (TILE_WIDTH / 2)
    y = (gx + gy) * (TILE_HEIGHT / 2)

    return int(x), int(y)


def draw_tile_iso(
        surface: pygame.Surface,
        gx: int,
        gy: int,
        color: tuple[int, int, int]
) -> None:
    iso_x, iso_y = grid_to_iso(gx, gy)

    cx = iso_x + SCREEN_WIDTH // 2
    cy = iso_y + 200

    top = (cx, cy - TILE_HEIGHT / 2)
    right = (cx + TILE_WIDTH / 2, cy)
    bottom = (cx, cy + TILE_HEIGHT / 2)
    left = (cx - TILE_WIDTH / 2, cy)

    pygame.draw.polygon(surface, color, [top, right, bottom, left])
    pygame.draw.polygon(surface, (0, 0, 0), [top, right, bottom, left], 1)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill((30, 30, 30))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    gx, gy = screen_to_grid(mouse_x, mouse_y)

    hovered_tile = None
    if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
        hovered_tile = (gx, gy)

    # Draw all tiles
    for gx in range(GRID_SIZE):
        for gy in range(GRID_SIZE):
            color = (100, 150, 100)
            
            if hovered_tile and hovered_tile == (gx, gy):
                color = (150, 200, 150)  # lighter green for hover
            
            draw_tile_iso(screen, gx, gy, color)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()
