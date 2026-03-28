import pygame

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    HUD_HEIGHT, HUD_COLOR, HUD_BORDER_COLOR
)


class Hud:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.y = SCREEN_HEIGHT - HUD_HEIGHT

    def render(self) -> None:
        pygame.draw.rect(
            self.screen,
            HUD_COLOR,
            (0, self.y, SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        pygame.draw.line(
            self.screen,
            HUD_BORDER_COLOR,
            (0, self.y),
            (SCREEN_WIDTH, self.y),
            3
        )