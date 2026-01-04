import pygame

from core.clock import GameClock
from core.events import EventManager


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1280, 800))
        pygame.display.set_caption("Buildings")

        self.clock = GameClock()
        self.events = EventManager()

        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick()

            self.events.process()
            if self.events.quit:
                self.running = False

