from __future__ import annotations
import math
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.enemy import Enemy
    from engine.player import Player

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,SCREEN_DIST,
    HALF_FOV,
    SPRITES_PATH
)
from engine.enemy import EnemyState


class SpriteRenderer:
    def __init__(
            self,
            screen: pygame.Surface
    ) -> None:
        self.screen = screen
        self._patrol_frame = self._load_single("rguard_s_1")
        self._chase_frames = [self._load_single(f"rguard_w{i}_1") for i in range(1, 5)]
        self._pain_frames = [self._load_single(f"rguard_pain{i}") for i in range(1, 3)]
        self._death_frames = [self._load_single(f"rguard_die{i}") for i in range(1, 5)]

    def _load_single(self, name: str) -> pygame.Surface:
        path = f"{SPRITES_PATH}guard/{name}.bmp"
        img = pygame.image.load(path).convert()
        img.set_colorkey(img.get_at((0, 0)))
        return img

    def render(
            self,
            enemies: list["Enemy"],
            player: "Player",
            z_buffer: list[float]
    ) -> None:
        sorted_enemies = sorted(
            enemies,
            key=lambda e: math.hypot(e.x - player.x, e.y - player.y),
            reverse=True
        )

        for enemy in sorted_enemies:
            dx = enemy.x - player.x
            dy = enemy.y - player.y
            dist = math.hypot(dx, dy)

            if dist < 0.1:
                continue

            enemy_angle = math.degrees(math.atan2(dy, dx)) - player.angle
            enemy_angle = (enemy_angle + 180) % 360 - 180

            if abs(enemy_angle) > HALF_FOV + 5:
                continue

            screen_x = int((enemy_angle / HALF_FOV + 1) * SCREEN_WIDTH / 2)
            sprite_height = int(SCREEN_DIST / dist)
            sprite_width = sprite_height

            top = SCREEN_HEIGHT // 2 - sprite_height // 2
            left = screen_x - sprite_width // 2

            if dist >= z_buffer[max(0, min(screen_x, SCREEN_WIDTH - 1))]:
                continue

            if enemy.state == EnemyState.DYING:
                frame = self._death_frames[min(enemy._anim_frame, 3)]
            elif enemy.state == EnemyState.PAIN:
                frame = self._pain_frames[min(enemy._anim_frame, 1)]
            else:
                frame = self._chase_frames[enemy._anim_frame % 4]

            scaled = pygame.transform.scale(frame, (sprite_width, sprite_height))
            self.screen.blit(scaled, (left, top))