from world.map import Map
from world.iso import Iso


class World:
    def __init__(self) -> None:
        self.map = Map(30, 30)
        self.map.generate()

        self.iso = Iso(title_width=64, title_height=32)

        self.map_offset = [400, 200]
        self.map_zoom = 1.0

        self.entities = []

    def update(self, dt: float):
        for entity in self.entities:
            entity.update(dt)
