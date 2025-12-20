import sys
import pygame
import random


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

TILE_WIDTH = 64
TILE_HEIGHT = 32

GRID_WIDTH = 30
GRID_HEIGHT = 30

ZOOM_MIN = 0.5
ZOOM_MAX = 2.0
ZOOM_STEP = 0.1

# Theme
MAIN_BACKGROUND_COLOR = (34, 139, 34)
TILE_BACKGROUND_COLOR = (0, 100, 0)
WHITE = (0, 0, 0)
WATER = (54, 117, 136)
SAND = (210, 180, 140)


def grid_to_iso(gx: int, gy: int, zoom: float) -> tuple[int, int]:
    tw = TILE_WIDTH * zoom
    th = TILE_HEIGHT * zoom

    x = (gx - gy) * (tw / 2)
    y = (gx + gy) * (th / 2)
    return int(x), int(y)


def screen_to_grid(
        mx: int,
        my: int,
        offset: list[int],
        zoom: float) -> tuple[int, int]:
    ox, oy = offset
    x = mx - ox
    y = my - oy

    tw = TILE_WIDTH * zoom
    th = TILE_HEIGHT * zoom

    gx = (y / (th / 2) + x / (tw / 2)) / 2
    gy = (y / (th / 2) - x / (tw / 2)) / 2

    return int(gx), int(gy)


def draw_tile(
        surface: pygame.Surface,
        gx: int,
        gy: int,
        color: tuple[int, int, int],
        offset: list[int],
        zoom: float,
        show_lines: bool) -> None:
    iso_x, iso_y = grid_to_iso(gx, gy, zoom)
    offset_x, offset_y = offset
    cx = iso_x + offset_x
    cy = iso_y + offset_y

    tw = TILE_WIDTH * zoom
    th = TILE_HEIGHT * zoom

    top = (cx, cy - th / 2)
    right = (cx + tw / 2, cy)
    bottom = (cx, cy + th / 2)
    left = (cx - tw / 2, cy)

    pygame.draw.polygon(
        surface,
        color,
        [top, right, bottom, left]
    )

    if show_lines:
        pygame.draw.polygon(
            surface,
            WHITE,
            [top, right, bottom, left],
            1
        )


def generate_empty_map(width, height):
    return [["grass" for _ in range(height)] for _ in range(width)]


def generate_river(map_data, min_radius=0, max_radius=2):
    width = len(map_data)
    height = len(map_data[0])
    orientation = random.choice(["horizontal", "vertical"])
    radius = random.randint(min_radius, max_radius)

    if orientation == "horizontal":
        x = 0
        y = random.randint(height // 4, 3 * height // 4)

        while 0 <= x < width:
            if random.random() < 0.12:
                radius += random.choice([-1, 1])
                radius = max(min_radius, min(max_radius, radius))

            for dy in range(-radius, radius + 1):
                ny = y + dy
                if 0 <= ny < height:
                    map_data[x][ny] = "water"

            x += 1

            if random.random() < 0.15:
                y += random.choice([-1, 1])

            y = max(radius + 1, min(height - radius - 2, y))

    elif orientation == "vertical":
        y = 0
        x = random.randint(width // 4, 3 * width // 4)

        while 0 <= y < width:
            if random.random() < 0.12:
                radius += random.choice([-1, 1])
                radius = max(min_radius, min(max_radius, radius))

            for dx in range(-radius, radius + 1):
                nx = x + dx
                if 0 <= nx < width:
                    map_data[nx][y] = "water"

            y += 1

            if random.random() < 0.15:
                x += random.choice([-1, 1])

            x = max(radius + 1, min(height - radius - 2, x))


def generate_sand(map_data):
    width = len(map_data)
    height = len(map_data[0])

    to_sand = []

    for x in range(width):
        for y in range(height):
            if map_data[x][y] != "grass":
                continue

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if map_data[nx][ny] == "water":
                        to_sand.append((x, y))
                        break

    for x, y in to_sand:
        map_data[x][y] = "sand"


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Buildings")
    clock = pygame.time.Clock()

    offset_x = SCREEN_WIDTH // 2
    offset_y = SCREEN_HEIGHT // (GRID_HEIGHT // 2)
    offset = [offset_x, offset_y]

    dragging = False
    last_mous_pos = (0, 0)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    zoom = 1.0

    map_data = generate_empty_map(GRID_WIDTH, GRID_HEIGHT)
    generate_river(map_data)
    generate_sand(map_data)

    show_lines = False
    show_hover = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mx, my = pygame.mouse.get_pos()

        hover_gx, hover_gy = screen_to_grid(mx, my, offset, zoom)

        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    show_lines = not show_lines

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    show_hover = not show_hover

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    dragging = True
                    last_mous_pos = event.pos
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    dragging = False
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if event.type == pygame.MOUSEMOTION and dragging:
                mx, my = event.pos
                lx, ly = last_mous_pos

                dx = mx - lx
                dy = my - ly

                offset[0] += dx
                offset[1] += dy

                last_mous_pos = event.pos

            if event.type == pygame.MOUSEWHEEL:
                old_zoom = zoom
                zoom += event.y * ZOOM_STEP
                zoom = max(ZOOM_MIN, min(ZOOM_MAX, zoom))


        # Idle Economy update


        # Draw update
        screen.fill(MAIN_BACKGROUND_COLOR)

        for gx in range(GRID_WIDTH):
            for gy in range(GRID_HEIGHT):
                tile_type = map_data[gx][gy]

                if tile_type == "water":
                    color = WATER
                elif tile_type == "sand":
                    color = SAND
                elif gx == hover_gx and gy == hover_gy and show_hover:
                    color = (200, 200, 50)
                else:
                    color = (TILE_BACKGROUND_COLOR)

                draw_tile(
                    surface=screen,
                    gx=gx,
                    gy=gy,
                    color=color,
                    offset=offset,
                    zoom=zoom,
                    show_lines=show_lines
                )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

