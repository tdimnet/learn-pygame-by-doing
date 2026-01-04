import pygame

from core.clock import GameClock
from core.events import EventManager

from render.renderer import Renderer


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1280, 800))
        pygame.display.set_caption("Buildings")

        self.clock = GameClock()
        self.events = EventManager()

        self.renderer = Renderer(self.screen)

        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick()

            self.events.process()
            if self.events.quit:
                self.running = False

            self.update(dt)
            self.draw()

    def update(self, dt: float):
        pass

    def draw(self):
        self.renderer.clear()
        pygame.display.flip()

