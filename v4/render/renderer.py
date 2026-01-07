import pygame


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def clear(self):
        self.screen.fill((30, 30, 30))

    def draw_world(self, world):
        for entity in world.entities:
            entity.draw(self.screen)

    def draw_ui(self, hud):
        hud.draw(self.screen)
