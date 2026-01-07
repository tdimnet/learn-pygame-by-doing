import pygame

from core.profiler import Profiler


class HUD:
    def __init__(self) -> None:
        self._font = pygame.font.SysFont(None, 18)
        self.show_profiler = True

    def update(self, dt, events, profiler):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_0]:
            profiler.toggle()

    def draw(self, screen):
        pass

    def draw_profiler(self, screen, profiler: Profiler):
        if not profiler.enabled:
            return

        x, y = 10, 10
        lines = [f"Frame: {profiler.frame_ms:.2f} ms  (~{(1000.0/profiler.frame_ms):.1f} FPS)" if profiler.frame_ms > 0 else "Frame: ..."]

        for name, last_ms, avg_ms, max_ms in profiler.snapshot()[:12]:
            lines.append(f"{name:<14} last {last_ms:6.2f}  avg {avg_ms:6.2f}  max {max_ms:6.2f}")

        for line in lines:
            surf = self._font.render(line, True, (240, 240, 240))
            screen.blit(surf, (x, y))
            y += 18
