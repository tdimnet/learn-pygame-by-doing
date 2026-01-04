import pygame


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

    def clear(self):
        self.screen.fill((30, 30, 30))

