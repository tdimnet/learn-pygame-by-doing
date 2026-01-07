class World:
    def __init__(self) -> None:
        self.entities = []

    def update(self, dt: float):
        for entity in self.entities:
            entity.update(dt)
