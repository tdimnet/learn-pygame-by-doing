from re import I
import sys
import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

TILE_WIDTH = 64
TILE_HEIGHT = 32

GRID_WIDTH = 10
GRID_HEIGHT = 10

MAIN_BACKGROUND_COLOR = (34, 139, 34)
TILE_BACKGROUND_COLOR = (0, 100, 0)
WHITE = (0, 0, 0)

TREE_SPRITE_PATH = "./assets/tree.png"


def grid_to_iso(gx: int, gy: int) -> tuple[int, int]:
    x = (gx - gy) * (TILE_WIDTH // 2)
    y = (gx + gy) * (TILE_HEIGHT // 2)
    return x, y


def draw_tile(
        surface: pygame.Surface,
        gx: int,
        gy: int,
        color: tuple[int, int, int],
        offset: tuple[int, int]) -> None:
    iso_x, iso_y = grid_to_iso(gx, gy)
    offset_x, offset_y = offset
    cx = iso_x + offset_x
    cy = iso_y + offset_y

    top = (cx, cy - TILE_HEIGHT // 2)
    right = (cx + TILE_WIDTH // 2, cy)
    bottom = (cx, cy + TILE_HEIGHT // 2)
    left = (cx - TILE_WIDTH // 2, cy)

    pygame.draw.polygon(
        surface,
        color,
        [top, right, bottom, left]
    )
    pygame.draw.polygon(
        surface,
        WHITE,
        [top, right, bottom, left],
        1
    )


def draw_tree(
        surface: pygame.Surface,
        sprite: pygame.Surface,
        gx: int,
        gy: int,
        offset: tuple[int, int],
        iso_cache: dict) -> None:
    iso_x, iso_y = iso_cache[(gx, gy)]
    offset_x, offset_y = offset

    px = iso_x + offset_x
    py = iso_y + offset_y

    sprite_rect = sprite.get_rect(midbottom=(px, py))
    surface.blit(sprite, sprite_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Buildings")
    clock = pygame.time.Clock()

    offset = (
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 4
    )

    tree_sprite = pygame.image.load("./assets/tree.png").convert_alpha()
    tree_sprite = pygame.transform.smoothscale(tree_sprite, (64, 128))


    iso_cache = {}
    for gx in range(GRID_WIDTH):
        for gy in range(GRID_HEIGHT):
            iso_cache[(gx, gy)] = grid_to_iso(gx, gy)

    trees = [
        (4, 5),
        (6, 3),
        (2, 7)
    ]


    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Idle economy update


        # Draw update
        screen.fill(MAIN_BACKGROUND_COLOR)

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
                    offset=offset
                )

        for gx, gy in sorted(trees, key=lambda t: t[0] + t[1]):
            iso_x, iso_y = iso_cache[(gx, gy)]
            px = iso_x + offset[0]
            py = iso_y + offset[1]

            sprite_rect = tree_sprite.get_rect(midbottom=(px, py))
            screen.blit(tree_sprite, sprite_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


