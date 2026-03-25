from typing import TYPE_CHECKING
import math
import pygame

if TYPE_CHECKING:
    from engine.map import Map


from config import (
    PLAYER_START_ANGLE,
    PLAYER_MAX_HEALTH,
    PLAYER_SPEED,
    PLAYER_ROT_SPEED
)

class Player:
    def __init__(self, map: "Map"):
        self.x, self.y = map.player_start
        self.angle = PLAYER_START_ANGLE
        self.health = PLAYER_MAX_HEALTH
        self.map = map

    def _try_move(self, new_x: int, new_y: int) -> None:
        if not self.map.is_wall(int(new_x), int(self.y)):
            self.x = new_x
        if not self.map.is_wall(int(self.x), int(new_y)):
            self.y = new_y

    def move(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        speed = PLAYER_SPEED * dt
        dx = math.cos(math.radians(self.angle)) * speed
        dy = math.sin(math.radians(self.angle)) * speed

        if keys[pygame.K_w]:
            self._try_move(self.x + dx, self.y + dy)
        if keys[pygame.K_s]:
            self._try_move(self.x - dx, self.y - dy)
        if keys[pygame.K_a]:
            self._try_move(self.x - dx, self.y + dy)
        if keys[pygame.K_d]:
            self._try_move(self.x + dx, self.y - dy)
    
    def rotate(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * dt * 100
        if keys[pygame.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * dt * 100
        
        self.angle %= 360
        
    def interact(self) -> None:
        ix = int(self.x + math.cos(math.radians(self.angle)))
        iy = int(self.y + math.sin(math.radians(self.angle)))

        self.map.open_door(ix, iy)