import sys
import pygame
import random


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
GRID_SIZE = 50

TILE_WIDTH = 64
TILE_HEIGHT = 32

COLORS = {
    "grass": (100, 150, 100),
    "water": (70, 130, 180),
    "sand": (230, 210, 160),
    "forest": (50, 100, 50),
    "mountain": (130, 130, 130),
}


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()


def screen_to_grid(
    screen_x: int,
    screen_y: int,
    camera_x: int,
    camera_y: int,
    zoom: float = 1.0
) -> tuple[int, int]:
    x = screen_x - camera_x
    y = screen_y - camera_y

    # Apply zoom to tile dimensions
    tw = TILE_WIDTH * zoom
    th = TILE_HEIGHT * zoom

    gx = (y / (th / 2) + x / (tw / 2)) / 2
    gy = (y / (th / 2) - x / (tw / 2)) / 2

    return int(gx), int(gy)


def grid_to_iso(
    gx: int,
    gy: int,
    zoom: float = 1.0
) -> tuple[int, int]:
    x = (gx - gy) * (TILE_WIDTH / 2) * zoom
    y = (gx + gy) * (TILE_HEIGHT / 2) * zoom

    return int(x), int(y)


def draw_tile_iso(
        surface: pygame.Surface,
        gx: int,
        gy: int,
        color: tuple[int, int, int],
        camera_x: int,
        camera_y: int,
        zoom: float
) -> None:
    iso_x, iso_y = grid_to_iso(gx, gy, zoom)

    # Apply your camera offset here
    cx = iso_x + camera_x
    cy = iso_y + camera_y

    # Scale tile dimensions by zoom
    tw = TILE_WIDTH * zoom
    th = TILE_HEIGHT * zoom

    # We replace
    top = (cx, cy - th / 2)
    right = (cx + tw / 2, cy)
    bottom = (cx, cy + th / 2)
    left = (cx - tw / 2, cy)

    pygame.draw.polygon(surface, color, [top, right, bottom, left])
    pygame.draw.polygon(surface, (0, 0, 0), [top, right, bottom, left], 1)


def generate_terrain(
    width: int,
    height: int,
    seed: int = None
) -> list[list[str]]:
    if seed is not None:
        random.seed(seed)

    terrain = [["grass" for _ in range(height)] for _ in range(width)]

    # We'll add river, sand, forest passes here

    return terrain


# Camera state
camera_x = SCREEN_WIDTH // 2
camera_y = 200
camera_speed = 10

# Zoom state
zoom = 1.0

# The terrain we generate
terrain = generate_terrain(GRID_SIZE, GRID_SIZE, seed=42)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            zoom += event.y * 0.1
            zoom = max(0.5, min(2.0, zoom))

    # Camera movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        camera_x += camera_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        camera_x -= camera_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        camera_y += camera_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        camera_y -= camera_speed

    screen.fill((30, 30, 30))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    gx, gy = screen_to_grid(
        mouse_x,
        mouse_y,
        camera_x,
        camera_y,
        zoom
    )

    hovered_tile = None
    if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
        hovered_tile = (gx, gy)

    # Draw all tiles
    for gx in range(GRID_SIZE):
        for gy in range(GRID_SIZE):
            tile = terrain[gx][gy]
            color = COLORS[tile]

            if hovered_tile and hovered_tile == (gx, gy):
                color = (150, 200, 150)  # lighter green for hover

            draw_tile_iso(
                screen,
                gx,
                gy,
                color,
                camera_x,
                camera_y,
                zoom
            )

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()

