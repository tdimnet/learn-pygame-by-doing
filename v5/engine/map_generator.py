import random
import math
from config import (
    RIVER_MIN_RADIUS, RIVER_MAX_RADIUS,
    FOREST_COUNT, FOREST_MIN_RADIUS, FOREST_MAX_RADIUS,
    MOUNTAIN_COUNT, MOUNTAIN_MIN_RADIUS, MOUNTAIN_MAX_RADIUS
)


def generate_empty_map(width: int, height: int) -> list[list[str]]:
    return [["grass" for _ in range(height)] for _ in range(width)]


def generate_river(
        map_data: list[list[str]],
        min_radius: int = RIVER_MIN_RADIUS,
        max_radius: int = RIVER_MAX_RADIUS) -> None:
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
                radius = max(min_radius, max(max_radius, radius))

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

        while 0 <= y < height:
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

            x = max(radius + 1, min(width - radius - 2, x))


def generate_sand(map_data: list[list[str]]) -> None:
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


def generate_forest(
        map_data: list[list[str]],
        forest_count: int = FOREST_COUNT,
        min_radius: int = FOREST_MIN_RADIUS,
        max_radius: int = FOREST_MAX_RADIUS) -> None:
    pass
