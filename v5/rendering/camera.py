import pygame
from config import (
    ZOOM_MIN, ZOOM_MAX, ZOOM_STEP,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    TILE_WIDTH, TILE_HEIGHT
)
from rendering.iso_utils import screen_to_grid


class Camera:
    def __init__(self, initial_offset_x: int, initial_offset_y: int) -> None:
        self.offset_x = initial_offset_x
        self.offset_y = initial_offset_y
        self.zoom = 1.0

        self.dragging = False
        self.last_mouse_pos = (0, 0)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.dragging = True
            self.last_mouse_pos = event.pos
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self.dragging = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            lx, ly = self.last_mouse_pos

            dx = mx - lx
            dy = my -ly

            self.offset_x += dx
            self.offset_y += dy

            self.last_mouse_pos = event.pos

        elif event.type == pygame.MOUSEWHEEL:
            old_zoom = self.zoom
            self.zoom += event.y * ZOOM_STEP
            self.zoom = max(ZOOM_MIN, min(ZOOM_MAX, self.zoom))

    def screen_to_grid(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        return screen_to_grid(
                screen_x, screen_y,
                self.offset_x, self.offset_y,
                self.zoom
        )

    def get_visible_tiles(self, grid_width: int, grid_height: int) -> list[tuple[int, int]]:
        top_left = self.screen_to_grid(0, 0)
        top_right = self.screen_to_grid(SCREEN_WIDTH, 0)
        bottom_left = self.screen_to_grid(0, SCREEN_HEIGHT)
        bottom_right = self.screen_to_grid(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Bounding box
        min_gx = max(0, min(top_left[0], top_right[0], bottom_left[0], bottom_right[0]) - 2)
        max_gx = min(grid_width, max(top_left[0], top_right[0], bottom_left[0], bottom_right[0]) + 2)
        min_gy = max(0, min(top_left[1], top_right[1], bottom_left[1], bottom_right[1]) - 2)
        max_gy = min(grid_height, max(top_left[1], top_right[1], bottom_left[1], bottom_right[1]) + 2)

        visible = []
        for gx in range(min_gx, max_gx + 1):
            for gy in range(min_gy, max_gy + 1):
                if 0 <= gx < grid_width and 0 <= gy < grid_height:
                    visible.append((gx, gy))

        return visible
