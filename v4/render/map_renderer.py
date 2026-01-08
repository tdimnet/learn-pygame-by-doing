import pygame

from world.iso import Iso


class MapRenderer:
    def __init__(self, iso: Iso, colors: dict) -> None:
        self.iso = iso
        self.colors = colors

    def draw_tile(self, screen, gx, gy, color, offset, zoom, show_lines):
        ix, iy = self.iso.grid_to_iso(gx, gy, zoom)
        cx = ix + offset[0]
        cy = yx + offset[1]

        tw = self.iso.title_width * zoom
        th = self.iso.title_height * zoom

        points = [
            (cx, cy - th / 2),
            (cx + tw / 2, cy),
            (cx, cy + th / 2),
            (cx - tw / 2, cy)
        ]

        pygame.draw.polygon(screen, color, points)
        if show_lines:
            pygame.draw.polygon(screen, (255, 255, 255), points, 1)

    def draw(self, screen, game_map, offset, zoom, show_lines=False,
             hover=None, show_hover=False):
        for gx in range(game_map.width):
            for gy in range(game_map.height):
                tile_type = game_map.tiles[gx][gy]
                color = self.colors.get(tile_type, (0, 100, 0))

                if show_hover and hover and (gx, gy) == hover:
                    color = (200, 200, 50)

                self.draw_tile(screen, gx, gy, color, offset, zoom, show_lines)
