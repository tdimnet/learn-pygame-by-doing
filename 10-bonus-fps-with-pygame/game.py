import pygame
import sys
import math

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    TITLE,
    FPS,
    SCREEN_DIST,
    HIT_TOLERANCE,
    HALF_FOV,
    WEAPONS
)
from engine.map import Map
from engine.player import Player
from engine.enemy import Enemy, EnemyState

from rendering.raycaster import Raycaster
from rendering.sprite_renderer import SpriteRenderer

from ui.hud import Hud
from ui.weapon import Weapon


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.map = Map("assets/maps/level_1.txt")
        self.player = Player(self.map)
        self.enemies = [Enemy(x, y) for x, y in self.map.enemy_positions]

        self.raycaster = Raycaster(self.screen, self.map, self.player)
        self.sprite_renderer = SpriteRenderer(self.screen)

        self.hud = Hud(self.screen)
        self.weapon = Weapon()

    def _try_shoot(self) -> None:
        candidates = []

        for enemy in self.enemies:
            if enemy.dead or enemy.state == EnemyState.DYING:
                continue

            dx = enemy.x - self.player.x
            dy = enemy.y - self.player.y
            dist = math.hypot(dx, dy)

            if dist < 0.1:
                continue

            enemy_angle = math.degrees(math.atan2(dy, dx)) - self.player.angle
            enemy_angle = (enemy_angle + 180) % 360 - 180

            if abs(enemy_angle) > HALF_FOV:
                continue

            screen_x = int((enemy_angle / HALF_FOV + 1) * SCREEN_WIDTH / 2)

            z = self.raycaster.z_buffer[max(0, min(screen_x, SCREEN_WIDTH - 1))]
            if dist >= z:
                continue

            sprite_width = int(SCREEN_DIST / dist)
            left = screen_x - sprite_width // 2
            right = screen_x + sprite_width // 2
            center = SCREEN_WIDTH // 2

            if left - HIT_TOLERANCE <= center <= right + HIT_TOLERANCE:
                candidates.append((dist, enemy))

        if candidates:
            candidates.sort(key=lambda c: c[0])
            _, nearest = candidates[0]
            nearest.take_damage(WEAPONS["pistol"]["damage"])

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.player.interact()
                    print("+++")
            
                if event.key == pygame.K_SPACE:
                    self.weapon.shoot()
                    self._try_shoot()

    def update(self, dt: float) -> None:
        self.player.move(dt)
        self.player.rotate(dt)

        for enemy in self.enemies:
            enemy.update(dt, self.player, self.map)
        # self.enemies = [e for e in self.enemies if not e.dead]
        
        self.weapon.update(dt)

    def draw(self) -> None:
        self.raycaster.render()
        self.sprite_renderer.render(
            self.enemies,
            self.player,
            self.raycaster.z_buffer
        )
        self.hud.render(
            level=1,
            score=0,
            lives=3,
            health=self.player.health,
            ammo=8
        )
        self.weapon.render(self.screen)