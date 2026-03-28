import pygame

from config import (
    WEAPON_FRAME_W,
    WEAPON_FRAME_H,
    WEAPON_SCALE,
    WEAPON_ROW,
    WEAPONS_SHEET,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    HUD_HEIGHT
)


class Weapon:
    FRAME_DURATION = 0.07

    def __init__(self) -> None:
        self._sheet = self._load_sheet()
        self._frames = self._extract_frames("pistol")
        self._current_frame = 0
        self._firing = False
        self._anim_timer = 0.0

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
    
    def shoot(self, dt: float) -> None:
        if not self._firing:
            self._firing = True
            self._current_frame = 1
            self._anim_timer = 0.0

    def update(self, dt: float) -> None:
        if not self._firing:
            return
        
        self._anim_timer += dt
        if self._anim_timer >= self.FRAME_DURATION:
            self._anim_timer = 0.0
            self._current_frame += 1
            if self._current_frame >= 5:
                self._current_frame = 0
                self._firing = False
    
    def render(self, screen: pygame.Surface) -> None:
        frame = self._frames[self._current_frame]

        scale_w = WEAPON_FRAME_W * WEAPON_SCALE
        scale_h = WEAPON_FRAME_H * WEAPON_SCALE
        scaled = pygame.transform.scale(frame, (scale_w, scale_h))

        x = (SCREEN_WIDTH - scale_w) // 2
        y = SCREEN_HEIGHT - HUD_HEIGHT - scale_h

        screen.blit(scaled, (x, y))