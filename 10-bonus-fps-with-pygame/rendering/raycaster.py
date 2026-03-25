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
        pass