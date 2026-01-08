import pygame

from core.clock import GameClock
from core.events import EventManager
from core.profiler import Profiler

from world.world import World
from ui.hud import HUD
from render.renderer import Renderer


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Buildings")

        self.clock = GameClock()
        self.events = EventManager()
        self.profiler = Profiler(enabled=False)

        self.world = World()
        self.hud = HUD()
        self.renderer = Renderer(self.screen)

        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick()

            self.profiler.reset_frame()

            self.events.process()
            if self.events.quit:
                self.running = False

            with self.profiler.section("update/world"):
                self.world.update(dt)

            with self.profiler.section("update/hud"):
                self.hud.update(dt, self.events, self.profiler)

            with self.profiler.section("draw/all"):
                self.draw()

            self.profiler.end_frame()

    def update(self, dt: float):
        self.world.update(dt)
        self.hud.update(dt, self.events, self.profiler)

    def draw(self):
        self.renderer.clear()

        with self.profiler.section("draw/clear"):
            self.renderer.clear()

        with self.profiler.section("draw/world"):
            self.renderer.draw_world(self.world)

        with self.profiler.section("draw/ui"):
            self.renderer.draw_ui(self.hud)

        self.hud.draw_profiler(self.screen, self.profiler)

        pygame.display.flip()
