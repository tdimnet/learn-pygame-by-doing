import pygame
from config import COLOR_UI_TEXT
from profiler import Profiler
from engine.game_state import GameState


class DebugOverlay:
    def __init__(self) -> None:
        self.enabled = False
        self.font = pygame.font.SysFont("monospace", 12)

    def toggle(self) -> None:
        self.enabled = not self.enabled

    def draw(
            self,
            surface: pygame.Surface,
            profiler: Profiler,
            game_state: GameState) -> None:
        if not self.enabled:
            return

        overlay_width = 350
        overlay_height = 300
        overlay_surface = pygame.Surface(
            (overlay_width, overlay_height),
            pygame.SRCALPHA
        )
        overlay_surface.fill((0, 0, 0, 180))

        y = 10
        line_height = 16

        fps_text = self.font.render(
            f"FPS: {int(1000 / profiler.frame_ms) if profiler.frame_ms > 0 else 0}",
            True,
            COLOR_UI_TEXT
        )
        overlay_surface.blit(fps_text, (10, y))
        y += line_height

        frame_text = self.font.render(
            f"Frame: {profiler.frame_ms:.2f}ms",
            True,
            COLOR_UI_TEXT
        )
        overlay_surface.blit(frame_text, (10, y))
        y += line_height * 2

        header = self.font.render(
            "Section              Last    Avg     Max",
            True,
            (200, 200, 200)
        )
        overlay_surface.blit(header, (10, y))
        y += line_height

        separator = self.font.render(
            "-" * 45,
            True,
            (100, 100, 100)
        )
        overlay_surface.blit(separator, (10, y))
        y += line_height

        snapshot = profiler.snapshot()
        for name, last_ms, avg_ms, max_ms in snapshot[:10]:
            display_name = name[:20].ljust(20)

            stats_text = self.font.render(
                f"{display_name} {last_ms:5.2f} {avg_ms:5.2f} {max_ms:5.2f}",
                True,
                COLOR_UI_TEXT
            )
            overlay_surface.blit(stats_text, (10, y))
            y += line_height

            buildings_text = self.font.render(
                f"Buildings: {game_state.grid.count_buildings()}",
                True,
                (150, 200, 150)
            )
            overlay_surface.blit(buildings_text, (10, y))

            surface.blit(
                overlay_surface,
                (surface.get_width() - overlay_width - 10, 10)
            )

