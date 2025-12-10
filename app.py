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


def draw_building(surface, gx, gy, offset, btype):
    colors = {
        "house": (50, 150, 255),
        "factory": (200, 60, 60),
        "powerplant": (230, 200, 60)
    }
    color = colors[btype]

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

    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (0, 0, 0), rect, 2)


def draw_tool_bar(surface, tool_buttons, selected):
    font = pygame.font.SysFont("arial", 18)

    for btn in tool_buttons:
        rect = btn["rect"]
        color = btn["color"]

        pygame.draw.rect(surface, color, rect)

        border_color = (0, 0, 0) if btn["type"] != selected else (255, 255, 255)
        pygame.draw.rect(surface, border_color, rect, 3)

        text = font.render(btn["type"].capitalize(), True, (0, 0, 0))
        text_x = rect.x + (rect.width - text.get_width()) // 2
        text_y = rect.y + (rect.height - text.get_height()) // 2
        surface.blit(text, (text_x, text_y))


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

    tool_buttons = [
        {
            "type": "house",
            "rect": pygame.Rect(10, 50, 120, 30),
            "color": (50, 150, 255)
        },
        {
            "type": "factory",
            "rect": pygame.Rect(140, 50, 120, 30),
            "color": (200, 60, 60)
        },
        {
            "type": "powerplant",
            "rect": pygame.Rect(270, 50, 140, 30),
            "color": (230, 200, 60)
        }
    ]
    selected_building = "house"

    gold = 50
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
                for btn in tool_buttons:
                    if btn["rect"].collidepoint(mx, my):
                        selected_building = btn["type"]
                        break
                else:
                    gx, gy = screen_to_grid(mx, my, offset)
                    if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                        if grid_data[gx][gy] == 0:
                            cost = BUILDINGS[selected_building]["cost"]
                            if gold >= cost:
                                gold -= cost
                                grid_data[gx][gy] = selected_building


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

            adjusted_gold_prod = total_gold_prod * pop_ratio
            adjusted_pop_prod = total_pop_prod - total_pop_consume

            population += adjusted_pop_prod
            if population < 0:
                population = 0

            gold += adjusted_gold_prod

            power = total_power_prod


        screen.fill(color=(60, 120, 180))

        draw_resource_bar(screen, gold, population, power)
        draw_tool_bar(screen, tool_buttons, selected_building)

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

                if grid_data[gx][gy] != 0:
                    draw_building(screen, gx, gy, offset,
                                  grid_data[gx][gy])

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

