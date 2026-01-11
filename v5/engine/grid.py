from config import GRID_WIDTH, GRID_HEIGHT


class Grid:
    """Handle the field grid and builded buildings"""

    def __init__(self, terrain: list[list[str]]) -> None:
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT

        self.terrain = terrain

        self.buildings = [[None for _ in range(self.height)] for _ in
                          range(self.width)]

        def is_valid_position(self, gx: int, gy: int) -> bool:
            return 0 <= gx < self.width and 0 <= gy < self.height

        def is_buildable(self, gx: int, gy: int) -> bool:
            if not self.is_valid_position(gx, gy):
                return False

            if self.terrain[gx][gy] == "water":
                return False

            if self.terrain[gx][gy] == "mountain":
                return False

            if self.buildings[gx][gy] is not None:
                return False

            return True
