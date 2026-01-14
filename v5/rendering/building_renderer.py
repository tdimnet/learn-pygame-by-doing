import pygame
from config import TILE_WIDTH, TILE_HEIGHT, BUILDINGS
from rendering.iso_utils import grid_to_iso


class BuildingRenderer:
    def __init__(self) -> None:
        pass

    def draw_building(
            self,
            surface: pygame.Surface,
            gx: int,
            gy: int,
            building_name: str, 
            camera_offset_x: int, 
            camera_offset_y: int, 
            zoom: float, 
            pop_effect: float = 0.0) -> None:
        iso_x, iso_y = grid_to_iso(gx, gy, zoom)
        cx = iso_x + camera_offset_x
        cy = iso_y + camera_offset_y

        tw = TILE_WIDTH * zoom
        th = TILE_HEIGHT * zoom
