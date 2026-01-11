import json
import os
from engine.grid import Grid
from config import BUILDINGS


class GameState:
    def __init__(self, terrain: list[list[str]]) -> None:
        self.grid = Grid(terrain)

        self.gold = 50
        self.population = 0
        self.power = 0

        self.harmony = 50.0
        self.harmony_time = 0.0  # Temps passé >= 70%
        self.harmony80_time = 0.0  # Temps passé >= 80%

        self.gold_per_sec = 0.0

        self.completed_milestones = set()

        self.idle_timer = 0.0

    def _update_economy(self):
        pass

    def can_place_building(self, gx: int, gy: int, building_name: str) -> bool:
        if not self.grid.is_buildable(gx, gy):
            return False

        cost = BUILDINGS[building_name]["cost"]
        if self.gold < cost:
            return False

        return True

    def place_building(self, gx: int, gy: int, building_name: str) -> bool:
        if not self.can_place_building(gx, gy, building_name):
            return False

        self.grid.place_building(gx, gy, building_name)

        cost = BUILDINGS[building_name]["cost"]
        self.gold -= cost

        return True

    def update(self, dt: float) -> None:
        self.idle_timer += dt

        if self.idle_timer >= 1.0:
            self.idle_timer = 0.0
            self._update_economy()
