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

    def _draw_items(
            self,
            menu_surface: pygame.Surface,
            items: list,
            start_y: int,
            offset_x: int,
            alpha: int) -> None:
        item_width = 80
        item_height = 80
        items_per_row = 3
        spacing = 20

        for i, building_name in enumerate(items):
            col = i % items_per_row
            row = i // items_per_row

            item_x = 30 + col * (item_width + spacing) + offset_x
            item_y = start_y + row * (item_height + spacing)

            item_rect = pygame.Rect(item_x, item_y, item_width, item_height)

            buiding_color = BUILDINGS[building_name]["color"]
            pygame.draw.rect(menu_surface, buiding_color, item_rect,
                             border_radius=8)

            cost = BUILDINGS[building_name]["cost"]
            cost_text = self.font_small.render(f"${cost}", True, (255, 255, 255))
            menu_surface.blit(cost_text, (item_x + 5, item_y + 5))

            name_text = self.font_small.render(building_name.capitalize(),
                                               True, (255, 255, 255))
            name_rect = name_text.get_rect(centerx=item_rect.centerx,
                                           bottom=item_rect.bottom - 5)
            menu_surface.blit(name_text, name_rect)

            self.item_rects[building_name] = pygame.Rect(
                self.x + item_x,
                self.y_open * self.anim_t + self.y_closed * (1 - self.anim_t) + item_y,
                item_width,
                item_height
            )

    def handle_click(self, mouse_pos: tuple[int, int]) -> dict:
        mx, my = mouse_pos

        for category, rect in self.category_rects.items():
            if rect.collidepoint(mx, my):
                if self.category_anim >= 1.0 and category != self.active_category:
                    self.previous_category = self.active_category
                    self.active_category = category
                    self.category_anim = 0.0

                return {"type": "category", "name": category}

        if self.category_anim >= 1.0:
            for building_name, rect in self.item_rects.items():
                if rect.collidepoint(mx, my):
                    return {
                        "type": "item",
                        "name": building_name
                    }

        return {
            "type": None,
            "name": None
        }

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

        content_y = 110

        slide_offset = int(self.width * (1 - self.category_anim))

        self.item_rects = {}

        if self.category_anim < 1.0 and self.previous_category:
            self._draw_items(
                menu_surface,
                BUILD_CATEGORIES[self.previous_category],
                content_y,
                -slide_offset,
                alpha
            )

        if self.category_anim < 1.0:
            offset_x = self.width - slide_offset
        else:
            offset_x = 0

        self._draw_items(
            menu_surface,
            BUILD_CATEGORIES[self.active_category],
            content_y,
            offset_x,
            alpha
        )

        surface.blit(menu_surface, (self.x, y))

        self.menu_rect = pygame.Rect(self.x, y, self.width, self.height)
