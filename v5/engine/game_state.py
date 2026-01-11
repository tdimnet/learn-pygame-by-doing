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
        house_count = self.grid.count_buildings("house")
        factory_count = self.grid.count_buildings("factory")
        powerplant_count = self.grid.count_buildings("powerplant")
        garden_count = self.grid.count_buildings("garden")
        park_count = self.grid.count_buildings("park")

        total_pop_prod = 0
        total_gold_prod = 0
        total_power_prod = 0
        total_pop_consume = 0

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                building = self.grid.buildings[x][y]
                if building is None:
                    continue

                props = BUILDINGS[building]
                total_pop_prod += props["pop_production"]
                total_gold_prod += props["gold_production"]
                total_power_prod += props["power_production"]
                total_pop_consume += props["pop_consume"]

        effective_factories = max(0, factory_count - park_count)

        harmony_delta = (
            2.0 * garden_count +
            5.0 * park_count +
            0.5 * house_count -
            1.0 * effective_factories
        ) * 0.05

        self.harmony += harmony_delta
        self.harmony = max(0.0, min(100.0, self.harmony))

        if self.harmony >= 70:
            self.harmony_time += 1
        else:
            self.harmony_time = max(0.0, self.harmony_time - 0.5)

        if self.harmony >= 80:
            self.harmony80_time += 1.0
        else:
            self.harmony80_time = max(0.0, self.harmony80_time - 0.5)

        total_pop_consume = max(0, total_pop_consume - garden_count)

        if total_pop_consume > 0:
            if self.population <= 0:
                pop_ratio = 0.0
            else:
                pop_ratio = min(1.0, self.population / total_pop_consume)
        else:
            pop_ratio = 1.0

        adjusted_gold_prod = total_gold_prod * pop_ratio

        power_boost = 1.0 + (0.2 * total_power_prod)
        adjusted_gold_prod *= power_boost

        if self.harmony >= 70:
            adjusted_gold_prod *= 1.10
        elif self.harmony <= 30:
            adjusted_gold_prod *= 0.90

        adjusted_pop_prod = total_pop_prod - total_pop_consume

        self.population += adjusted_pop_prod
        self.population = max(0, self.population)

        self.gold += adjusted_gold_prod
        self.gold_per_sec = adjusted_gold_prod

        self.power = total_power_prod

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

    def save(self, filename: str = "save.json") -> None:
        data = {
            "gold": self.gold,
            "population": self.population,
            "power": self.power,
            "harmony": self.harmony,
            "harmony_time": self.harmony_time,
            "harmony80_time": self.harmony80_time,
            "buildings": self.grid.buildings,
            "completed_milestones": list(self.completed_milestones)
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Game saved: {filename}")

    @staticmethod
    def load(terrain: list[list[str]], filename: str = "save.json") -> 'GameState':
        if not os.path.exists(filename):
            print("No saved game found, launching new game")
            return GameState(terrain)

        try:
            with open(filename, "r") as f:
                data = json.load(f)

            state = GameState(terrain)
            state.gold = data.get("gold", 50)
            state.population = data.get("population", 0)
            state.power = data.get("power", 0)
            state.harmony = data.get("harmony", 50.0)
            state.harmony_time = data.get("harmony_time", 0.0)
            state.harmony80_time = data.get("harmony80_time", 0.0)
            state.grid.buildings = data.get("buildings", state.grid.buildings)
            state.completed_milestones = set(data.get("completed_milestones", []))

            print(f"Jeu chargé : {filename}")
            return state

        except Exception as e:
            print(f"Error when loading the game: {e}. Launching new game")
            return GameState(terrain)
