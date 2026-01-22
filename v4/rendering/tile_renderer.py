import pygame
from pygame.draw import polygon
from config import (
    TILE_WIDTH, TILE_HEIGHT,
    COLOR_GRASS, COLOR_GRASS_ALT,
    COLOR_WATER, COLOR_SAND,
    COLOR_FOREST, COLOR_MOUNTAIN
)
from rendering.iso_utils import grid_to_iso


class TileRenderer:
    BIOME_COLORS = {
        "grass": COLOR_GRASS,
        "grass_alt": COLOR_GRASS_ALT,
        "water": COLOR_WATER,
        "sand": COLOR_SAND,
        "forest": COLOR_FOREST,
        "mountain": COLOR_MOUNTAIN
    }

    def __init__(self) -> None:
        pass

    def draw_tile(
            self,
            surface: pygame.Surface,
            gx: int,
            gy: int,
            terrain_type: str,
            camera_offset_x: int,
            camera_offset_y: int,
            zoom: float,
            show_grid: bool = True) -> None:
        iso_x, iso_y = grid_to_iso(gx, gy, zoom)

        cx = iso_x + camera_offset_x
        cy = iso_y + camera_offset_y

        tw = TILE_WIDTH * zoom
        th = TILE_HEIGHT * zoom

        top = (cx, cy - th / 2)
        right = (cx + tw / 2, cy)
        bottom = (cx, cy + th / 2)
        left = (cx - tw / 2, cy)

        if terrain_type == "grass":
            if (gx + gy) % 2 == 0:
                color = self.BIOME_COLORS["grass"]
            else:
                color = self.BIOME_COLORS["grass_alt"]
        else:
            color = self.BIOME_COLORS.get(terrain_type, COLOR_GRASS)

        pygame.draw.polygon(surface, color, [top, right, bottom, left])

        if show_grid:
            pygame.draw.polygon(
                surface,
                (0, 0, 0),
                [top, right, bottom, left],
                1
            )

    def draw_terrain(
            self,
            surface: pygame.Surface,
            terrain: list[list[str]],
            visible_tiles: list[tuple[int, int]],
            camera_offset_x: int,
            camera_offset_y: int,
            zoom: float,
            show_grid: bool = True) -> None:
        for gx, gy in visible_tiles:
            terrain_type = terrain[gx][gy]

            self.draw_tile(
                surface,
                gx, gy,
                terrain_type,
                camera_offset_x,
                camera_offset_y,
                zoom,
                show_grid
            )
