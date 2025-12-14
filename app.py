import json
import os
import sys

import pygame


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
    },
    "garden": {
        "cost": 30,
        "pop_production": 1,
        "gold_production": 0,
        "power_production": 0,
        "pop_consume": 0,
    }
}

MILESTONES = [
    {
        "id": "gold_100",
        "condition": lambda city, cities: city["gold"] >= 100,
        "reward": lambda city, cities: city.update({
            "gold": city["gold"] + 50
        }),
        "message": "Premiers pas : +50 gold"
    },
    {
        "id": "houses_5",
        "condition": lambda city, cities:
            sum(1 for x in city["grid"] for y in x if y == "house") >= 5,
        "reward": lambda city, cities: city.update({
            "population": city["population"] + 2
        }),
        "message": "Quartier résidentiel : la population grandit"
    },
    {
        "id": "factories_5",
        "condition": lambda city, cities:
            sum(1 for x in city["grid"] for y in x if y == "factory") >= 5,
        "reward": lambda city, cities: city.update({
            "gold": city["gold"] + 100
        }),
        "message": "Ville active : +100 gold"
    },
    {
        "id": "unlock_city_2",
        "condition": lambda city, cities:
            city.get("gold_per_sec", 0) >= 20 and len(cities) < 2,
        "reward": lambda city, cities: cities.append(create_empty_city()),
        "message": "Nouvelle ville débloquée"
    },
    {
        "id": "garden_1",
        "condition": lambda city, cities:
            sum(1 for x in city["grid"] for y in x if y == "garden") >= 1,
        "reward": lambda city, cities: cities.append({
            city["population"] + 3
        }),
        "message": "Un jardin apporte de la sérénité"
    },
]


def create_empty_city():
    return {
        "grid": [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)],
        "gold": 50,
        "population": 0,
        "power": 0,
        "pop_effect": [[0 for _ in range(GRID_HEIGHT)] for _ in
                       range(GRID_WIDTH)],
        "gold_per_sec": 0
    }


def save_game(cities, current_city, completed_milestones, filename="save.json"):
    data = {
        "cities": cities,
        "current_city": current_city,
        "completed_milestones": list(completed_milestones)
    }
    with open (filename, "w") as f:
        json.dump(data, f)


def load_game(filename="save.json"):
    if not os.path.exists(filename):
        return None

    with open(filename, "r") as f:
        data = json.load(f)

    cities = data.get("cities", [])
    if not isinstance(cities, list):
        cities = []

    current_city = data.get("current_city", 0)
    completed_milestones = set(data.get("completed_milestones", []))

    if not cities:
        cities = [create_empty_city()]
        current_city = 0

    return {
        "cities": cities,
        "current_city": current_city,
        "completed_milestones": completed_milestones
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


def draw_building(surface, gx, gy, offset, btype, pop_time=0):
    colors = {
        "house": (50, 150, 255),
        "factory": (200, 60, 60),
        "powerplant": (230, 200, 60),
        "garden" : (80, 180, 120)
    }
    color = colors[btype]

    iso_x, iso_y = grid_to_iso(gx, gy)
    ox, oy = offset
    cx = iso_x + ox
    cy = iso_y + oy

    base_duration = 0.15
    if pop_time > 0:
        scale = 1.0 + (pop_time / base_duration) * 0.25
    else:
        scale = 1.0

    building_width = int((TILE_WIDTH // 2) * scale)
    building_height = int(TILE_HEIGHT * scale)

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


def draw_iso_outline(surface, gx, gy, offset, color, width=3):
    iso_x, iso_y = grid_to_iso(gx, gy)
    ox, oy = offset
    cx, cy = iso_x + ox, iso_y + oy

    top = (cx, cy - TILE_HEIGHT // 2)
    right = (cx + TILE_WIDTH // 2, cy)
    bottom = (cx, cy + TILE_HEIGHT // 2)
    left = (cx - TILE_WIDTH // 2, cy)

    pygame.draw.polygon(surface, color, [top, right, bottom, left], width)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Buildings")
    clock = pygame.time.Clock()

    offset = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

    tool_buttons = [
        {"type": "house",      "rect": pygame.Rect(10, 50, 120, 30), "color": (50, 150, 255)},
        {"type": "factory",    "rect": pygame.Rect(140, 50, 120, 30), "color": (200, 60, 60)},
        {"type": "powerplant", "rect": pygame.Rect(270, 50, 140, 30), "color": (230, 200, 60)},
        {"type": "garden", "rect": pygame.Rect(420, 50, 120, 30), "color": (80, 180, 120)},
    ]
    selected_building = "house"

    completed_milestones = set()
    milestone_popup_timer = 0
    milestone_popup_text = ""


    pop_effect = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    prev_city_button = pygame.Rect(550, 50, 40, 30)
    next_city_button = pygame.Rect(600, 50, 40, 30)

    loaded = load_game()
    if loaded:
        cities = loaded["cities"]
        current_city = loaded["current_city"]
        completed_milestones = loaded["completed_milestones"]
    else:
        cities = [create_empty_city()]
        current_city = 0
        completed_milestones = set()

    idle_timer = 0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mx, my = pygame.mouse.get_pos()

        def city():
            return cities[current_city]

        hover_gx, hover_gy = screen_to_grid(mx, my, offset)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(cities, current_city, completed_milestones)
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_tool = False
                for btn in tool_buttons:
                    if btn["rect"].collidepoint(mx, my):
                        selected_building = btn["type"]
                        clicked_tool = True
                        break

                if clicked_tool:
                    continue

                if prev_city_button.collidepoint(mx, my):
                    if current_city > 0:
                        current_city -= 1
                    continue

                if next_city_button.collidepoint(mx, my):
                    current_city += 1
                    if current_city >= len(cities):
                        cities.append(create_empty_city())
                    continue

                gx, gy = screen_to_grid(mx, my, offset)
                if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
                    if city()["grid"][gx][gy] == 0:
                        cost = BUILDINGS[selected_building]["cost"]
                        if city()["gold"] >= cost:
                            city()["gold"] -= cost
                            city()["grid"][gx][gy] = selected_building
                            city()["pop_effect"][gx][gy] = 0.15 


        # Idle Economy update
        idle_timer += dt
        if idle_timer >= 1.0:
            idle_timer = 0

            for c in cities:
                total_pop_prod = 0
                total_gold_prod = 0
                total_power_prod = 0
                total_pop_consume = 0

                grid = c["grid"]

                for gx in range(GRID_WIDTH):
                    for gy in range(GRID_HEIGHT):
                        b = grid[gx][gy]
                        if b == 0:
                            continue

                        props = BUILDINGS[b]
                        total_pop_prod += props["pop_production"]
                        total_gold_prod += props["gold_production"]
                        total_power_prod += props["power_production"]
                        total_pop_consume += props["pop_consume"]

                garden_count = sum(
                    1 for gx in range(GRID_WIDTH)
                    for gy in range(GRID_HEIGHT)
                    if grid[gx][gy] == "garden"
                )

                total_pop_consume = max(0, total_pop_consume - garden_count)


                population = c["population"]
                if total_pop_consume > 0:
                    if population <= 0:
                        pop_ratio = 0
                    else:
                        pop_ratio = min(1.0, population / total_pop_consume)
                else:
                    pop_ratio = 1.0

                adjusted_gold_prod = total_gold_prod * pop_ratio
                adjusted_pop_prod = total_pop_prod - total_pop_consume

                power_val = c["power"]
                boost = 1 + (0.2 * power_val)
                adjusted_gold_prod *= boost

                population += adjusted_pop_prod
                if population < 0:
                    population = 0
                c["population"] = population

                c["gold"] += adjusted_gold_prod
                c["gold_per_sec"] = adjusted_gold_prod
                c["power"] = total_power_prod


        for m in MILESTONES:
            if m["id"] not in completed_milestones:
                if m["condition"](city(), cities):
                    m["reward"](city(), cities)
                    completed_milestones.add(m["id"])
                    milestone_popup_text = m["message"]
                    milestone_popup_timer = 2.5

        for gx in range(GRID_WIDTH):
            for gy in range(GRID_HEIGHT):
                if city()["pop_effect"][gx][gy] > 0:
                    city()["pop_effect"][gx][gy] -= dt
                    if city()["pop_effect"][gx][gy] < 0:
                        city()["pop_effect"][gx][gy] = 0

        screen.fill((60, 120, 180))

        draw_resource_bar(
            screen,
            int(city()["gold"]),
            int(city()["population"]),
            int(city()["power"])
        )
        draw_tool_bar(screen, tool_buttons, selected_building)

        pygame.draw.rect(screen, (180, 180, 180), prev_city_button)
        pygame.draw.rect(screen, (180, 180, 180), next_city_button)
        font = pygame.font.SysFont("arial", 20)
        screen.blit(font.render("<", True, (0, 0, 0)),
                    (prev_city_button.x + 12, prev_city_button.y + 2))
        screen.blit(font.render(">", True, (0, 0, 0)),
                    (next_city_button.x + 12, next_city_button.y + 2))
        city_label = font.render(f"Ville {current_city + 1}", True, (255, 255, 255))
        screen.blit(city_label, (450, 15))

        for gx in range(GRID_WIDTH):
            for gy in range(GRID_HEIGHT):
                grid = city()["grid"]

                if gx == hover_gx and gy == hover_gy:
                    tile_color = (200, 200, 50)
                else:
                    tile_color = (100, 180, 100) if (gx + gy) % 2 == 0 else (80, 160, 80)

                draw_tile(screen, gx, gy, tile_color, offset)

                if gx == hover_gx and gy == hover_gy:
                    outline_color = (255, 255, 255) if grid[gx][gy] == 0 else (255, 80, 80)
                    draw_iso_outline(screen, gx, gy, offset, outline_color, 3)

                if grid[gx][gy] != 0:
                    draw_building(
                        screen,
                        gx,
                        gy,
                        offset,
                        grid[gx][gy],
                        city()["pop_effect"][gx][gy],
                    )


        if milestone_popup_timer > 0:
            milestone_popup_timer -= dt
            font = pygame.font.SysFont("arial", 22)
            text = font.render(
                milestone_popup_text,
                True,
                (255, 255, 100)
            )
            screen.blit(
                text,
                (SCREEN_WIDTH // 2 - text.get_width() // 2, 120)
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

