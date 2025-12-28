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


def grid_to_iso(gx: int, gy: int) -> tuple[int, int]:
    x = (gx - gy) * (TILE_WIDTH // 2)
    y = (gx + gy) * (TILE_HEIGHT // 2)
    return x, y


def screen_to_grid(mx: int, my: int, offset: tuple[int, int]) -> tuple[int, int]:
    ox, oy = offset
    x = mx - ox
    y = my - oy

    gx = (y / (TILE_HEIGHT / 2) + x / (TILE_WIDTH / 2)) / 2
    gy = (y / (TILE_HEIGHT / 2) - x / (TILE_WIDTH / 2)) / 2

    return int(gx), int(gy)


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


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Buildings")
    clock = pygame.time.Clock()

    offset = (
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 4
    )

    placing_tree = False
    placing_house = False
    placing_shop = False
    placing_bakery = False

    tree_sprite = pygame.image.load("./assets/tree.png").convert_alpha()
    tree_sprite = pygame.transform.smoothscale(tree_sprite, (64, 128))

    house_sprite = pygame.image.load("./assets/house.png").convert_alpha()
    house_sprite = pygame.transform.smoothscale(house_sprite,
                                                (128, 128))

    shop_sprite = pygame.image.load("./assets/shop.png").convert_alpha()
    shop_sprite = pygame.transform.smoothscale(shop_sprite,
                                                (128, 128))

    bakery_sprite = pygame.image.load("./assets/bakery.png").convert_alpha()
    bakery_sprite = pygame.transform.smoothscale(bakery_sprite,
                                                (128, 128))

    iso_cache = {}
    for gx in range(GRID_WIDTH):
        for gy in range(GRID_HEIGHT):
            iso_cache[(gx, gy)] = grid_to_iso(gx, gy)

    trees = [
        (4, 5),
        (6, 3),
        (2, 7)
    ]
    houses = []
    shops = []
    bakeries = []


    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mx, my = pygame.mouse.get_pos()

        hover_gx, hover_gy = screen_to_grid(mx, my, offset)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    placing_tree = not placing_tree

                if event.key == pygame.K_h:
                    placing_house = not placing_house

                if event.key == pygame.K_s:
                    placing_shop = not placing_shop

                if event.key == pygame.K_b:
                    placing_bakery = not placing_bakery

            if event.type == pygame.MOUSEBUTTONDOWN and placing_tree:
                gx, gy = screen_to_grid(mx, my, offset)

                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    trees.append((gx, gy))
                    placing_tree = False

            if event.type == pygame.MOUSEBUTTONDOWN and placing_house:
                gx, gy = screen_to_grid(mx, my, offset)

                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    houses.append((gx, gy))
                    placing_house = False

            if event.type == pygame.MOUSEBUTTONDOWN and placing_shop:
                gx, gy = screen_to_grid(mx, my, offset)

                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    shops.append((gx, gy))
                    placing_shop = False

            if event.type == pygame.MOUSEBUTTONDOWN and placing_bakery:
                gx, gy = screen_to_grid(mx, my, offset)

                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    bakeries.append((gx, gy))
                    placing_bakery = False

        # Idle economy update


        # Draw update
        screen.fill(MAIN_BACKGROUND_COLOR)

        for gx in range(GRID_WIDTH):
            for gy in range(GRID_HEIGHT):
                if (gx + gy) % 2 == 0:
                    color = (100, 180, 100)
                else:
                    color = (80, 160, 80)

                if gx == hover_gx and gy == hover_gy:
                    color = (200, 200, 50)

                draw_tile(
                    surface=screen,
                    gx=gx,
                    gy=gy,
                    color=color,
                    offset=offset
                )

        if placing_tree:
            gx, gy = screen_to_grid(mx, my, offset)

            if (gx, gy) in iso_cache:
                iso_x, iso_y = iso_cache[(gx, gy)]
                px = iso_x + offset[0]
                py = iso_y + offset[1] + TILE_HEIGHT

                ghost_rect = tree_sprite.get_rect(midbottom=(px, py))
                ghost = tree_sprite.copy()
                ghost.set_alpha(120)
                screen.blit(ghost, ghost_rect)

        if placing_house:
            gx, gy = screen_to_grid(mx, my, offset)

            if (gx, gy) in iso_cache:
                iso_x, iso_y = iso_cache[(gx, gy)]
                px = iso_x + offset[0]
                py = iso_y + offset[1] + TILE_HEIGHT

                ghost_rect = house_sprite.get_rect(midbottom=(px, py))
                ghost = house_sprite.copy()
                ghost.set_alpha(120)
                screen.blit(ghost, ghost_rect)

        if placing_shop:
            gx, gy = screen_to_grid(mx, my, offset)

            if (gx, gy) in iso_cache:
                iso_x, iso_y = iso_cache[(gx, gy)]
                px = iso_x + offset[0]
                py = iso_y + offset[1] + TILE_HEIGHT

                ghost_rect = shop_sprite.get_rect(midbottom=(px, py))
                ghost = shop_sprite.copy()
                ghost.set_alpha(120)
                screen.blit(ghost, ghost_rect)

        if placing_bakery:
            gx, gy = screen_to_grid(mx, my, offset)

            if (gx, gy) in iso_cache:
                iso_x, iso_y = iso_cache[(gx, gy)]
                px = iso_x + offset[0]
                py = iso_y + offset[1] + TILE_HEIGHT

                ghost_rect = bakery_sprite.get_rect(midbottom=(px, py))
                ghost = bakery_sprite.copy()
                ghost.set_alpha(120)
                screen.blit(ghost, ghost_rect)

        for gx, gy in sorted(trees, key=lambda t: t[0] + t[1]):
            iso_x, iso_y = iso_cache[(gx, gy)]
            px = iso_x + offset[0]
            py = iso_y + offset[1] + TILE_HEIGHT

            sprite_rect = tree_sprite.get_rect(midbottom=(px, py))
            screen.blit(tree_sprite, sprite_rect)

        for gx, gy in sorted(houses, key=lambda t: t[0] + t[1]):
            iso_x, iso_y = iso_cache[(gx, gy)]
            px = iso_x + offset[0]
            py = iso_y + offset[1] + TILE_HEIGHT

            sprite_rect = house_sprite.get_rect(midbottom=(px, py))
            screen.blit(house_sprite, sprite_rect)

        for gx, gy in sorted(shops, key=lambda t: t[0] + t[1]):
            iso_x, iso_y = iso_cache[(gx, gy)]
            px = iso_x + offset[0]
            py = iso_y + offset[1] + TILE_HEIGHT

            sprite_rect = shop_sprite.get_rect(midbottom=(px, py))
            screen.blit(shop_sprite, sprite_rect)

        for gx, gy in sorted(bakeries, key=lambda t: t[0] + t[1]):
            iso_x, iso_y = iso_cache[(gx, gy)]
            px = iso_x + offset[0]
            py = iso_y + offset[1] + TILE_HEIGHT

            sprite_rect = bakery_sprite.get_rect(midbottom=(px, py))
            screen.blit(bakery_sprite, sprite_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()


