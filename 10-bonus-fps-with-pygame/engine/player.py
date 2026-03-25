from typing import TYPE_CHECKING
import math

if TYPE_CHECKING:
    from engine.map import Map


from config import (
    PLAYER_START_ANGLE,
    PLAYER_MAX_HEALTH
)

class Player:
    def __init__(self, map: "Map"):
        self.x, self.y = map.player_start
        self.angle = PLAYER_START_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.map = map

    def _try_move(self, new_x: int, new_y: int) -> None:
        if not self.map.is_wall(int(new_x), int(self.y)):
            self.x = new_x
        if not self.map.is_wall(int(self.x), int(new_y)):
            self.y = new_y

    def move(self):
        pass
    
    def rotate(self):
        pass

    def interact(self):
        pass