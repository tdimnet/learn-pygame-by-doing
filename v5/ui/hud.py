import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_UI_BG, COLOR_UI_TEXT,
    COLOR_BUTTON_NORMAL, COLOR_BUTTON_HOVER, COLOR_BUTTON_SELECTED
)


class HUD:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("arial", 20)
        self.font_small = pygame.font.SysFont("arial", 14)

        self.height = 120

        self.buttons = {}

    def draw(
            self,
            surface: pygame.Surface,
            gold: int,
            population: int,
            power: int,
            harmony: float,
            mouse_pos: tuple[int, int],
            active_menu: str = None) -> dict:

        return {}
