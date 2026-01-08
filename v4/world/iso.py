from dataclasses import dataclass


@dataclass(frozen=True)
class Iso:
    title_width: int
    title_height: int

    def grid_to_iso(self, gx: int, gy: int, zoom: float = 1.0) -> tuple[int, int]:
        tw = self.title_height * zoom
        th = self.title_height * zoom
        x = (gx - gy) * (tw / 2)
        y = (gx + gy) * (th / 2)
        return int(x), int(y)

    def screen_to_grid(self, x: int, y: int, zoom: float = 1.0) -> tuple[int, int]:
        tw = self.title_width * zoom
        th = self.title_height * zoom
        gx = (y / (th / 2) + x / (tw / 2)) / 2
        gy = (y / (th / 2) - x / (tw / 2)) / 2
        return int(gx), int(gy)
