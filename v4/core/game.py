import pygame

from core.events import EventManager


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1280, 800))
        pygame.display.set_caption("Buildings")

        self.events = EventManager()

        self.running = True

    def run(self):
        while self.running:

            self.events.process()
            if self.events.quit:
                self.running = False

