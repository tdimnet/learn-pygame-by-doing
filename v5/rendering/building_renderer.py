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

        if pop_effect > 0:
            scale = 1.0 + pop_effect * 0.25
        else:
            scale = 1.0

        building_width = int((tw / 2) * scale)
        building_height = int(th * scale)

        color = BUILDINGS[building_name]["color"]

        rect = pygame.Rect(
            cx - building_width // 2,
            cy - building_height,
            building_width,
            building_height
        )

        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)

    def draw_buildings(
            self,
            surface: pygame.Surface,
            grid,
            visible_tiles: list[tuple[int, int]],
            camera_offset_x: int,
            camera_offset_y: int,
            zoom: float,
            pop_effects: list[list[float]] = None) -> None:
        for gx, gy in visible_tiles:
            building = grid.buildings[gx][gy]

            if building is not None:
                pop_effect = 0.0
                if pop_effects is not None:
                    pop_effect = pop_effects[gx][gy]

                self.draw_building(
                    surface,
                    gx, gy,
                    building,
                    camera_offset_x,
                    camera_offset_y,
                    zoom,
                    pop_effect
                )
