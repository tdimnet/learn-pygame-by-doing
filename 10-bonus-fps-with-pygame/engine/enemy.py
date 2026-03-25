from __future__ import annotations
import math
from enum import Enum, auto
from typing import TYPE_CHECKING
from config import (
    ENEMY_SPEED,
    ENEMY_DETECTION_RANGE
)

if TYPE_CHECKING:
    from engine.map import Map
    from engine.player import Player


class EnemyState(Enum):
    PATROL = auto()
    CHASE = auto()


class Enemy:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.state = EnemyState.PATROL

        # Patrol state
        self._start_x = x
        self._start_y = y
        self._patrol_dir = 1.0

    def _move_towards(
            self,
            tx: float,
            ty: float,
            speed: float,
            map: "Map"
    ) -> None:
        dx = tx - self.x
        dy = ty - self.y

        length = math.hypot(dx, dy)
        if length < 0.05:
            return
        
        dx, dy = dx / length * speed, dy / length * speed

        new_x = self.x + dx
        new_y = self.y + dy

        if not map.is_wall(int(new_x), int(self.y)):
            self.x = new_x
        if not map.is_wall(int(self.x), int(new_y)):
            self.y = new_y

    def _update_patrol(self):
        pass

    def _update_chase(self):
        pass

    def distance_to_player(self):
        pass

    def update(self):
        pass