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

        self.top_height = 70
        self.bottom_height = 60

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
        top_surface = pygame.Surface((SCREEN_WIDTH, self.top_height), pygame.SRCALPHA)
        top_surface.fill((*COLOR_UI_BG, 210))
        surface.blit(top_surface, (0, 0))

        gold_text = self.font.render(f"Gold: {gold}", True, COLOR_UI_TEXT)
        pop_text = self.font.render(f"Population: {population}", True, COLOR_UI_TEXT)
        power_text = self.font.render(f"Power: {power}", True, COLOR_UI_TEXT)

        surface.blit(gold_text, (20, 15))
        surface.blit(pop_text, (180, 15))
        surface.blit(power_text, (380, 15))

        harmony_x = 20
        harmony_y = 45
        harmony_width = 300
        harmony_height = 12
        pygame.draw.rect(
            surface,
            (40, 40, 40),
            (harmony_x, harmony_y, harmony_width, harmony_height),
            border_radius=6
        )

        harmony = max(0, min(100, harmony))
        fill_width = int((harmony / 100) * harmony_width)

        if harmony >= 70:
            harmony_color = (100, 200, 120)
        elif harmony >= 40:
            harmony_color = (200, 200, 120)
        else:
            harmony_color = (200, 100, 100)

        pygame.draw.rect(
            surface,
            harmony_color,
            (harmony_x, harmony_y, fill_width, harmony_height),
            border_radius=6
        )

        harmony_text = self.font_small.render(
            f"Harmonie {int(harmony)}%",
            True,
            COLOR_UI_TEXT
        )
        surface.blit(harmony_text, (harmony_x + harmony_width + 10, harmony_y - 2))

        # Bottom bar
        bottom_y = SCREEN_HEIGHT - self.bottom_height

        bottom_surface = pygame.Surface(
            (SCREEN_WIDTH, self.bottom_height),
            pygame.SRCALPHA
        )
        bottom_surface.fill((*COLOR_UI_BG, 210))
        surface.blit(bottom_surface, (0, bottom_y))

        button_width = 80
        button_height = 40
        button_spacing = 10
        button_y = bottom_y + (self.bottom_height - button_height) // 2

        build_x = SCREEN_WIDTH - 200
        build_rect = pygame.Rect(build_x, button_y, button_width, button_height)

        stats_x = SCREEN_WIDTH - 110
        stats_rect = pygame.Rect(stats_x, button_y, button_width, button_height)

        if active_menu == "build":
            build_color = COLOR_BUTTON_SELECTED
        elif build_rect.collidepoint(mouse_pos):
            build_color = COLOR_BUTTON_HOVER
        else:
            build_color = COLOR_BUTTON_NORMAL

        pygame.draw.rect(surface, build_color, build_rect, border_radius=8)
        build_text = self.font.render("Build", True, COLOR_UI_TEXT)
        build_rect_text = build_text.get_rect(center=build_rect.center)
        surface.blit(build_text, build_rect_text)

        if active_menu == "stats":
            stats_color = COLOR_BUTTON_SELECTED
        elif stats_rect.collidepoint(mouse_pos):
            stats_color = COLOR_BUTTON_HOVER
        else:
            stats_color = COLOR_BUTTON_NORMAL

        pygame.draw.rect(surface, stats_color, stats_rect, border_radius=8)
        stats_text = self.font.render("Stats", True, COLOR_UI_TEXT)
        stats_rect_text = stats_text.get_rect(center=stats_rect.center)
        surface.blit(stats_text, stats_rect_text)

        self.buttons = {
            "build": build_rect,
            "stats": stats_rect
        }

        return self.buttons
