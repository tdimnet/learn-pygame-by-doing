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

    def update(self, dt: float, is_open: bool) -> None:
        if is_open:
            self.anim_t = min(1.0, self.anim_t + dt * self.anim_speed)
        else:
            self.anim_t = max(0.0, self.anim_t - dt * self.anim_speed)

        if self.category_anim < 1.0:
            self.category_anim = min(1.0, self.category_anim + dt *
                                     self.category_anim_speed)

            if self.category_anim >= 1.0:
                self.previous_category = ""

    def draw(self, surface: pygame.Surface, mouse_pos: tuple[int, int]) -> None:
        if self.anim_t <= 0.0:
            self.menu_rect = None
            return

        y = self.y_closed + (self.y_open - self.y_closed) * self.anim_t
        alpha = int(255 * self.anim_t)

        menu_surface = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        )
        menu_surface.fill((30, 40, 30, alpha))

        title = self.font.render("Construction", True, (*COLOR_UI_TEXT, alpha))
        menu_surface.blit(title, (20, 15))

        self.category_rects = {}
        tab_x = 20
        tab_y = 55
        tab_width = 120
        tab_height = 35

        for category in BUILD_CATEGORIES.keys():
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)

            is_hover = tab_rect.collidepoint(mouse_pos[0] - self.x,
                                             mouse_pos[1] - y)
            is_active = (category == self.active_category)

            if is_active:
                tab_color = COLOR_BUTTON_SELECTED
            elif is_hover:
                tab_color = COLOR_BUTTON_HOVER
            else:
                tab_color = COLOR_BUTTON_NORMAL

            pygame.draw.rect(menu_surface, tab_color, tab_rect, border_radius=6)

            tab_text = self.font_small.render(category, True, COLOR_UI_TEXT)
            text_rect = tab_text.get_rect(center=tab_rect.center)
            menu_surface.blit(tab_text, text_rect)

            self.category_rects[category] = pygame.Rect(
                self.x + tab_x,
                y + tab_y,
                tab_width,
                tab_height
            )

            tab_x += tab_width + 10
