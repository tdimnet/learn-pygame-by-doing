import pygame
import sys


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

TILE_WIDTH = 64
TILE_HEIGHT = 32

GRID_WIDTH = 10
GRID_HEIGHT = 10

BUILDINGS = {
    "house": {
        "cost": 10,
        "pop_production": 1,
        "gold_production": 0,
        "power_production": 0,
        "pop_consume": 0,
    },
    "factory": {
        "cost": 20,
        "pop_production": 0,
        "gold_production": 2,
        "power_production": 0,
        "pop_consume": 1,
    },
    "powerplant": {
        "cost": 50,
        "pop_production": 0,
        "gold_production": 0,
        "power_production": 1,
        "pop_consume": 1,
    }
}


def draw_resource_bar(surface, gold, population, power):
    bar_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 40)
    pygame.draw.rect(surface, (30, 30, 30), bar_rect)

    font = pygame.font.SysFont("arial", 20)

    gold_text = font.render(f"Gold: {gold}", True, (255, 215, 0))
    pop_text = font.render(f"Population: {population}", True, (100, 200, 255))
    power_text = font.render(f"Power: {power}", True, (200, 200, 255))

    surface.blit(gold_text, (10, 10))
    surface.blit(pop_text, (150, 10))
    surface.blit(power_text, (350, 10))


def grid_to_iso(gx: int, gy: int) -> tuple[int, int]:
    x = (gx - gy) * (TILE_WIDTH // 2)
    y = (gx + gy) * (TILE_HEIGHT // 2)
    return x, y


def screen_to_grid(mx: int, my: int, offset: tuple[int, int]):
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


def draw_building(surface, gx, gy, offset):
    iso_x, iso_y = grid_to_iso(gx, gy)
    ox, oy = offset
    cx = iso_x + ox
    cy = iso_y + oy

    building_width = TILE_WIDTH // 2
    building_height = TILE_HEIGHT

    rect = pygame.Rect(
        cx - building_width // 2,
        cy - building_height,
        building_width,
        building_height
    )

    pygame.draw.rect(surface, (160, 50, 50), rect)
    pygame.draw.rect(surface, (0, 0, 0), rect, 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(
        title="Buildings"
    )
    clock = pygame.time.Clock()
 
    offset_x = SCREEN_WIDTH // 2
    offset_y = SCREEN_HEIGHT // 4
    offset = (offset_x, offset_y)

    gold = 100
    population = 0
    power = 0

    idle_timer = 0

    grid_data = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        mx, my = pygame.mouse.get_pos()
        hover_gx, hover_gy = screen_to_grid(mx, my, offset)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gx, gy = screen_to_grid(mx, my, offset)
                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    if grid_data[gx][gy] == 0:
                        cost = BUILDINGS["factory"]["cost"]
                        if gold >= cost:
                            gold -= cost
                            grid_data[gx][gy] = "factory"


        # ------------------ IDLE ECONOMY UPDATE ------------------
        idle_timer += dt
        if idle_timer >= 1.0:
            idle_timer = 0

            total_pop_prod = 0
            total_gold_prod = 0
            total_power_prod = 0
            total_pop_consume = 0

            for gx in range(GRID_WIDTH):
                for gy in range(GRID_HEIGHT):
                    b = grid_data[gx][gy]
                    if b == 0:
                        continue

                    props = BUILDINGS[b]
                    total_pop_prod += props["pop_production"]
                    total_gold_prod += props["gold_production"]
                    total_power_prod += props["power_production"]
                    total_pop_consume += props["pop_consume"]

            if total_pop_consume > 0:
                if population <= 0:
                    pop_ratio = 0
                else:
                    pop_ratio = min(1.0, population / total_pop_consume)
            else:
                pop_ratio = 1.0

            print("====")
            print(pop_ratio)
            print("====")


        screen.fill(color=(60, 120, 180))

        draw_resource_bar(screen, gold, population, power)

        for gx in range(GRID_WIDTH):
            for gy in range(GRID_HEIGHT):

                # Update on hover
                if gx == hover_gx and gy == hover_gy:
                    color = (200, 200, 50)
                # Draw the grid with different color
                else:
                    color = (100, 180, 100) if (gx + gy) % 2 == 0 else (80, 160, 80)

                draw_tile(
                    surface=screen,
                    gx=gx,
                    gy=gy,
                    color=color,
                    offset=offset)

                if grid_data[gx][gy] == 1:
                    draw_building(screen, gx, gy, offset)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

