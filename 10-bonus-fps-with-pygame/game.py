import pygame
import sys

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    TITLE,
    FPS
)
from engine.map import Map
from engine.player import Player
from engine.enemy import Enemy

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
            
                if event.type == pygame.K_SPACE:
                    print("+++")

    def update(self, dt: float) -> None:
        self.player.move(dt)
        self.player.rotate(dt)

        for enemy in self.enemies:
            enemy.update(dt, self.player, self.map)
        
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