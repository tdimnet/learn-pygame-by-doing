from __future__ import annotations
import math
from enum import Enum, auto
from typing import TYPE_CHECKING
from config import (
    ENEMY_SPEED,
    ENEMY_DETECTION_RANGE
)

if TYPE_CHECKING:
    from engine.map import Map
    from engine.player import Player


class EnemyState(Enum):
    PATROL = auto()
    CHASE = auto()


class Enemy:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.state = EnemyState.PATROL

        # Patrol state
        self._start_x = x
        self._start_y = y
        self._patrol_dir = 1.0

        # Animation
        self._anim_timer = 0.0
        self._anim_frame = 0
    
    def _update_animation(self, dt: float) -> None:
        frame_duration = 0.15 if self.state == EnemyState.CHASE else 0.25
        self._anim_timer += dt
        if self._anim_timer >= frame_duration:
            self._anim_timer = 0.0
            self._anim_frame = (self._anim_frame + 1) % 8

    def _move_towards(
            self,
            tx: float,
            ty: float,
            speed: float,
            map: "Map"
    ) -> None:
        dx = tx - self.x
        dy = ty - self.y

        length = math.hypot(dx, dy)
        if length < 0.05:
            return
        
        dx, dy = dx / length * speed, dy / length * speed

        new_x = self.x + dx
        new_y = self.y + dy

        if not map.is_wall(int(new_x), int(self.y)):
            self.x = new_x
        if not map.is_wall(int(self.x), int(new_y)):
            self.y = new_y

    def _update_patrol(
            self,
            dt: float,
            map: "Map"
    ) -> None:
        target_x = self._start_x + self._patrol_dir * 1.5
        target_y = self._start_y

        self._move_towards(target_x, target_y, ENEMY_SPEED * dt, map)

        next_x = self._start_x + self._patrol_dir * 1.5
        if (math.hypot(next_x - self.x, self._start_y - self.y) < 0.1
            or map.is_wall(int(next_x), int(self._start_y))):
                self._patrol_dir *= -1

    def _update_chase(
            self,
            dt: float,
            player: "Player",
            map: "Map"
    ) -> None:
        self._move_towards(player.x, player.y, ENEMY_SPEED * dt, map)

    def distance_to_player(
            self,
            player: "Player"
    ) -> float:
        return math.hypot(player.x - self.x, player.y - self.y)

    def update(
            self,
            dt: float,
            player: "Player",
            map: "Map"
    ) -> None:
        dist = self.distance_to_player(player)

        if self.state == EnemyState.PATROL and dist < ENEMY_DETECTION_RANGE:
            self.state = EnemyState.CHASE
        elif self.state == EnemyState.CHASE and dist > ENEMY_DETECTION_RANGE * 1.2:
            self.state = EnemyState.PATROL
        
        if self.state == EnemyState.PATROL:
            self._update_patrol(dt, map)
        elif self.state == EnemyState.CHASE:
            self._update_chase(dt, player, map)
        
        self._update_animation(dt)