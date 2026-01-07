import pygame

from core.clock import GameClock
from core.events import EventManager

from world.world import World
from ui.hud import HUD
from render.renderer import Renderer


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1280, 800))
        pygame.display.set_caption("Buildings")

        self.clock = GameClock()
        self.events = EventManager()

        self.world = World()
        self.hud = HUD()
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
        self.world.update(dt)
        self.hud.update(dt, self.events)

    def draw(self):
        self.renderer.clear()
        self.renderer.draw_world(self.world)
        self.renderer.draw_ui(self.hud)
        pygame.display.flip()

