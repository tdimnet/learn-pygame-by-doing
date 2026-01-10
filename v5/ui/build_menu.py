import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_UI_BG, COLOR_UI_TEXT,
    COLOR_BUTTON_NORMAL, COLOR_BUTTON_HOVER, COLOR_BUTTON_SELECTED,
    BUILDINGS, BUILD_CATEGORIES
)


class BuildMenu:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("Arial", 20)
        self.font_small = pygame.font.SysFont("arial", 14)

        self.width = 400
        self.height = 300

        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y_closed = SCREEN_HEIGHT
        self.y_open = SCREEN_HEIGHT - 60 - self.height - 10

        self.anim_t = 0.0
        self.anim_speed = 6.0

        self.active_category = "Résidentiel"
        self.previous_category = ""
        self.category_anim = 1.0
        self.category_anim_speed = 8.0

        self.menu_rect = None
        self.category_rects = {}
        self.item_rects = {}

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pass
