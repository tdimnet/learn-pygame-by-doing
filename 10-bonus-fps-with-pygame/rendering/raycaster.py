from typing import TYPE_CHECKING
import pygame
import math

if TYPE_CHECKING:
    from engine.map import Map
    from engine.player import Player

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    NUM_RAYS, HALF_FOV, DELTA_ANGLE,
    SCREEN_DIST, MAX_DEPTH,
    FLOOR_COLOR, CEILING_COLOR
)


class Raycaster:
    def __init__(
            self,
            screen: pygame.Surface,
            map: "Map",
            player: "Player"
    ) -> None:
        self.screen = screen
        self.map = map
        self.player = player

    def cast_ray(self, angle: float) -> float:
        ray_cos = math.cos(math.radians(angle))
        ray_sin = math.sin(math.radians(angle))

        if ray_cos == 0: ray_cos = 1e-6
        if ray_sin == 0: ray_sin = 1e-6

        map_x = int(self.player.x)
        map_y = int(self.player.y)

        delta_x = abs(1 / ray_cos)
        delta_y = abs(1 / ray_sin)

        if ray_cos < 0:
            stex_x = -1
            side_dist_x = (self.player.x - map_x) * delta_x
        else:
            stex_x = 1
            side_dist_x = (map_x + 1 - self.player.x) * delta_x

        if ray_sin < 0:
            stex_y = -1
            side_dist_y = (self.player.y - map_y) * delta_y
        else:
            stex_y = 1
            side_dist_y = (map_y + 1 - self.player.y) * delta_y

        hit = False
        side = 0

        for _ in range(MAX_DEPTH):
            if side_dist_x < side_dist_y:
                side_dist_x += delta_x
                map_x += stex_x
                side = 0
            else:
                side_dist_y += delta_y
                map_y += stex_y
                side = 1

            if self.map.is_wall(map_x, map_y):
                hit = True
                break
        
        if side == 0:
            perp_dist = (map_x - self.player.x + (1 - stex_x) / 2) / ray_cos
        else:
            perp_dist = (map_y - self.player.y + (1 - stex_y) / 2) / ray_sin
        
        return max(perp_dist, 0.0001)

    def render(self) -> None:
        pygame.draw.rect(
            self.screen,
            CEILING_COLOR,
            (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        )
        pygame.draw.rect(
            self.screen,
            FLOOR_COLOR,
            (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        )

        for ray in range(NUM_RAYS):
            angle = self.player.angle - HALF_FOV + ray * DELTA_ANGLE
            dist = self.cast_ray(angle)

            wall_height = int(SCREEN_DIST / dist)
            wall_top = max(0, SCREEN_HEIGHT // 2 - wall_height // 2)
            wall_bottom = min(SCREEN_HEIGHT, SCREEN_HEIGHT // 2 + wall_height // 2)

            shade = max(40, 255 - int(dist * 20))
            color = (shade, shade // 2, shade // 2)

            pygame.draw.line(
                self.screen,
                color,
                (ray, wall_top),
                (ray, wall_bottom)
            )