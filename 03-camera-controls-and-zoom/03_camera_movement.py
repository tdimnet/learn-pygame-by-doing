import sys
import pygame


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
GRID_SIZE = 50

TILE_WIDTH = 64
TILE_HEIGHT = 32


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()


def screen_to_grid(
    screen_x: int,
    screen_y: int,
    camera_x: int,
    camera_y: int
) -> tuple[int, int]:
    x = screen_x - camera_x
    y = screen_y - camera_y

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
        color: tuple[int, int, int],
        camera_x: int,
        camera_y: int
) -> None:
    iso_x, iso_y = grid_to_iso(gx, gy)

    # Apply your camera offset here
    cx = iso_x + camera_x
    cy = iso_y + camera_y

    top = (cx, cy - TILE_HEIGHT / 2)
    right = (cx + TILE_WIDTH / 2, cy)
    bottom = (cx, cy + TILE_HEIGHT / 2)
    left = (cx - TILE_WIDTH / 2, cy)

    pygame.draw.polygon(surface, color, [top, right, bottom, left])
    pygame.draw.polygon(surface, (0, 0, 0), [top, right, bottom, left], 1)


# Camera state
camera_x = SCREEN_WIDTH // 2
camera_y = 200
camera_speed = 10


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
        camera_y
    )

    hovered_tile = None
    if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
        hovered_tile = (gx, gy)

    # Draw all tiles
    for gx in range(GRID_SIZE):
        for gy in range(GRID_SIZE):
            color = (100, 150, 100)

            if hovered_tile and hovered_tile == (gx, gy):
                color = (150, 200, 150)  # lighter green for hover

            draw_tile_iso(
                screen,
                gx,
                gy,
                color,
                camera_x,
                camera_y
            )

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()

