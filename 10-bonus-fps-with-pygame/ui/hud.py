import pygame

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    HUD_HEIGHT, HUD_COLOR, HUD_BORDER_COLOR,
    HUD_TEXT_COLOR, HUD_LABEL_COLOR
)


class Hud:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.y = SCREEN_HEIGHT - HUD_HEIGHT
        self._font_label = pygame.font.SysFont("Arial", 16, bold=True)
        self._font_value = pygame.font.SysFont("Arial", 32, bold=True)

    def _draw_section(
            self,
            label: str,
            value: str,
            cx: int
    ) -> None:
        label_surf = self._font_label.render(label, True, HUD_LABEL_COLOR)
        label_rect = label_surf.get_rect(centerx=cx, top=self.y + 12)
        self.screen.blit(label_surf, label_rect)

        value_surf = self._font_value.render(value, True, HUD_TEXT_COLOR)
        value_rect = value_surf.get_rect(centerx=cx, top=self.y + 32)
        self.screen.blit(value_surf, value_rect)

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