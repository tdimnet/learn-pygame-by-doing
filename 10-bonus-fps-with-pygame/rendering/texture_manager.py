import pygame

from config import (
    TEXTURES_PATH,
    WALL_TEXTURES,
    TILE_SIZE
)


class TextureManager:
    def __init__(self) -> None:
        self._textures: dict[int, pygame.Surface] = {}
        self._load_all()

    def _load_all(self) -> None:
        for tile_id, filename in WALL_TEXTURES.items():
            path = TEXTURES_PATH + filename
            img = pygame.image.load(path).convert()
            self._textures[tile_id] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    def get_column(
            self,
            tile_id: int,
            tex_x: int,
            column_height: int
    ) -> pygame.Surface:
        texture = self._textures.get(tile_id, self._textures[1])
        column = texture.subsurface(pygame.Rect(tex_x, 0, 1, TILE_SIZE))
        return pygame.transform.scale(column, (1, column_height))