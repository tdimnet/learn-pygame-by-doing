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
    def __init__(self):
        pass

    def _move_towards(self):
        pass

    def _update_patrol(self):
        pass

    def _update_chase(self):
        pass

    def distance_to_player(self):
        pass

    def update(self):
        pass