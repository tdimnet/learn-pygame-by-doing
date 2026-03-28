import pygame

from config import (
    WEAPON_FRAME_W,
    WEAPON_FRAME_H,
    WEAPON_SCALE,
    WEAPON_ROW,
    WEAPONS_SHEET
)


class Weapon:
    def __init__(self) -> None:
        self._sheet = self._load_sheet()
        self._frames = self._extract_frames("pistol")
        self._current_frame = 0

    def _load_sheet(self) -> pygame.Surface:
        img = pygame.image.load(WEAPONS_SHEET).convert()
        img.set_colorkey((0, 0, 0))
        return img

    def _extract_frames(self, name: str) -> list[pygame.Surface]:
        row = WEAPON_ROW[name]
        frames = []
        for col in range(5):
            rect = pygame.Rect(
                col * WEAPON_FRAME_W,
                row * WEAPON_FRAME_H,
                WEAPON_FRAME_W,
                WEAPON_FRAME_H
            )
            frame = self._sheet.subsurface(rect).copy()
            frames.append(frame)
        return frames