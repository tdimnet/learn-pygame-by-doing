class Map:
    def __init__(self, filename: str) -> None:
        self.grid = []
        self.player_start = None
        self.enemy_positions = []
        self._load(filename)

    def _load(self, filename: str) -> None:
        with open(filename, "r") as f:
            for y, line in enumerate(f.readlines()):
                row = []
                for x, char in enumerate(line.strip()):
                    if char == "P":
                        self.player_start = (x + 0.5, y + 0.5)
                        row.append(0)
                    elif char == "E":
                        self.enemy_positions.append((x + 0.5, y + 0.5))
                        row.append(0)
                    else:
                        row.append(int(char))
                self.grid.append(row)

    def get_tile(self, x: int, y: int) -> int:
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
            return self.grid[x][y]
        return 1
    
    def is_wall(self, x: int, y: int) -> bool:
        return self.get_tile(x, y) in (1, 2, 3)

    def is_door(self, x:int, y: int) -> bool:
        return self.get_tile(x, y) == 4

    def open_door(self, x: int, y: int):
        if self.is_door(x, y):
            self.grid[x][y] = 0