import sys
import pygame


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
GRID_SIZE= 10

TILE_WIDTH = 64
TILE_HEIGHT = 32


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()


def draw_tile_topdown(
    surface: pygame.Surface,
    gx: int,
    gy: int,
    color: tuple[int, int, int]
) -> None:
    x = gx * TILE_SIZE + 200 # offset to center the grid
    y = gy * TILE_SIZE + 100

    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(surface, color, rect) # Draw the title
    pygame.draw.rect(
        surface,
        (0, 0, 0),
        rect,
        1
    ) # Draw the border around the tile


def get_tile_at_mouse(
        mouse_x: int,
        mouse_y: int
) -> tuple[int, int] | None:
    # Reverse the calculation from draw_tilte_topdown
    gx = (mouse_x - 200) // TILE_SIZE
    gy = (mouse_y - 100) // TILE_SIZE

    if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
        return gx, gy
    
    return None


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
    hovered_tile = get_tile_at_mouse(mouse_x, mouse_y)

    # Draw all tiles
    for gx in range(GRID_SIZE):
        for gy in range(GRID_SIZE):
            draw_tile_iso(screen, gx, gy, (100, 150, 100))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()