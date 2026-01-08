import random
import math
from typing import List


Tile = str  # "grass", "water"


class Map:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles: List[List[Tile]] = [["grass" for _ in range(height)] for _
                                        in range(width)]

    def generated(self):
        generate_river(self.tiles)


def generate_river(map_data, min_radius=0, max_radius=2):
    width = len(map_data)
    height = len(map_data[0])
    orientation = "horizontal"
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

