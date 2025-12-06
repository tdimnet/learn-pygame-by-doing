import pygame
import sys


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

TILE_WIDTH = 64
TILE_HEIGHT = 32

GRID_WIDTH = 10
GRID_HEIGHT = 10


def grid_to_iso(gx: int, gy: int) -> tuple[int, int]:
    x = (gx - gy) * (TILE_WIDTH // 2)
    y = (gx + gy) * (TILE_HEIGHT // 2)
    return x, y


def draw_tile(
    surface: pygame.Surface,
    gx: int,
    gy: int,
    color: tuple[int, int, int],
    offset: tuple[int, int]):
    iso_x, iso_y = grid_to_iso(gx, gy)
    offset_x, offset_y = offset
    cx = iso_x + offset_x
    cy = iso_y + offset_y

    top = (cx, cy - TILE_HEIGHT // 2)
    right = (cx + TILE_WIDTH // 2, cy)
    bottom = (cx, cy + TILE_HEIGHT // 2)
    left = (cx - TILE_WIDTH // 2, cy)

    pygame.draw.polygon(
        surface=surface,
        color=color,
        points=[top, right, bottom, left]
    )
    pygame.draw.polygon(
        surface=surface,
        color=(0, 0, 0),
        points=[top, right, bottom, left],
        width=1
    )


def main():
    pygame.init()
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(
        title="Buildings"
    )
    clock = pygame.time.Clock()
 
    offset_x = SCREEN_WIDTH // 2
    offset_y = SCREEN_HEIGHT // 2
    offset = (offset_x, offset_y)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(color=(60, 120, 180))

        for gx in range(GRID_WIDTH):
            for gy in range(GRID_HEIGHT):
                if (gx + gy) % 2 == 0:
                    color = (100, 180, 100)
                else:
                    color = (80, 160, 80)

                draw_tile(
                    surface=screen,
                    gx=gx,
                    gy=gy,
                    color=color,
                    offset=offset)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

