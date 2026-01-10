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
        hud_rect = pygame.Rect(0, 0, SCREEN_WIDTH, self.height)
        hud_surface = pygame.Surface((SCREEN_WIDTH, self.height), pygame.SRCALPHA)
        hud_surface.fill((*COLOR_UI_BG, 210))
        surface.blit(hud_surface, (0, 0))

        gold_text = self.font.render(f"Gold: {gold}", True, COLOR_UI_TEXT)
        pop_text = self.font.render(f"Population: {population}", True, COLOR_UI_TEXT)
        power_text = self.font.render(f"Power: {power}", True, COLOR_UI_TEXT)

        surface.blit(gold_text, (20, 15))
        surface.blit(pop_text, (180, 15))
        surface.blit(power_text, (380, 15))

        harmony_x = 20
        harmony_y = 50
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
            harmony_color = (100, 200, 100)
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
        surface.blit(
            harmony_text,
            (harmony_x + harmony_width + 10, harmony_y - 2)
        )


        return {}
