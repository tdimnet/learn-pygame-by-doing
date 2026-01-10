import sys
import pygame

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    GRID_WIDTH, GRID_HEIGHT
)
from engine.map_generator import generate_terrain
from rendering.camera import Camera
from rendering.tile_renderer import TileRenderer


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Buildings")
    clock = pygame.time.Clock()

    print("Generating game field")
    terrain = generate_terrain(GRID_WIDTH, GRID_HEIGHT)
    print(f"Field generated: {GRID_WIDTH} x {GRID_HEIGHT}")

    camera = Camera(
        initial_offset_x=SCREEN_WIDTH // 2,
        initial_offset_y=SCREEN_HEIGHT // 4
    )

    tile_renderer = TileRenderer()

    show_grid = True
    show_hover = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mx, my = pygame.mouse.get_pos()

        hover_gx, hover_gy = camera.screen_to_grid(mx, my)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    show_grid = not show_grid
                    print(f"Grid lines: {'On' if show_grid else 'Off'}")

                if event.key == pygame.K_h:
                    show_hover = not show_hover
                    print(f"Hover highlight: {'ON' if show_hover else 'OFF'}")

            camera.handle_event(event)

        screen.fill((34, 139, 34))

        visible_tiles = camera.get_visible_tiles(GRID_WIDTH, GRID_HEIGHT)
        tile_renderer.draw_terrain(
            screen,
            terrain,
            visible_tiles,
            camera.offset_x,
            camera.offset_y,
            camera.zoom,
            show_grid
        )

        if show_hover and 0 <= hover_gx < GRID_WIDTH and 0 <= hover_gy < GRID_HEIGHT:
            tile_renderer.draw_tile(
                screen,
                hover_gx, hover_gy,
                "grass_alt",
                camera.offset_x,
                camera.offset_y,
                camera.zoom,
                show_grid=False
            )

        font = pygame.font.SysFont("arial", 14)
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        zoom_text = font.render(f"Zoom: {camera.zoom:.2f}", True, (255, 255, 255))
        tiles_text = font.render(f"Tiles drawn: {len(visible_tiles)}/{GRID_WIDTH * GRID_HEIGHT}", True, (255, 255, 255))

        screen.blit(fps_text, (10, 10))
        screen.blit(zoom_text, (10, 30))
        screen.blit(tiles_text, (10, 50))

        if show_hover and 0 <= hover_gx < GRID_WIDTH and 0 <= hover_gy < GRID_HEIGHT:
            hover_text = font.render(
                f"Tile: ({hover_gx}, {hover_gy}) - {terrain[hover_gx][hover_gy]}",
                True,
                (255, 255, 255)
            )
            screen.blit(hover_text, (10, 70))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
