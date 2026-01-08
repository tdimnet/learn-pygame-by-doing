import pygame

from render.map_renderer import MapRenderer


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.colors = {
            "grass": (0, 100, 0),
            "water": (54, 117, 136)
        }
        self.map_renderer = None

    def clear(self):
        self.screen.fill((30, 30, 30))

    def draw_world(self, world):
        if self.map_renderer is None:
            self.map_renderer = MapRenderer(world.iso, self.colors)

        self.map_renderer.draw(
            screen=self.screen,
            game_map=world.map,
            offset=world.map_offset,
            zoom=world.map_zoom,
            show_lines=False,
        )

    def draw_ui(self, hud):
        hud.draw(self.screen)

        if hasattr(hud, "draw_profiler") and hasattr(hud, "profiler_ref"):
            hud.draw_profiler((self.screen, hud.profiler_ref))
