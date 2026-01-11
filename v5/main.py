import sys
import pygame

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    GRID_WIDTH, GRID_HEIGHT
)
from engine.map_generator import generate_terrain
from rendering.camera import Camera
from rendering.tile_renderer import TileRenderer
from ui.hud import HUD
from ui.build_menu import BuildMenu


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
    hud = HUD()
    build_menu = BuildMenu()

    mock_gold = 500
    mock_population = 10
    mock_power = 5
    mock_harmony = 70.0

    current_menu = None
    selected_building = None

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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hud.buttons.get("build") and hud.buttons["build"].collidepoint(mx, my):
                    current_menu = "build" if current_menu != "build" else None
                    selected_building = None

                elif hud.buttons.get("stats") and hud.buttons["stats"].collidepoint(mx, my):
                    current_menu = "stats" if current_menu != "stats" else None
                    selected_building = None

                elif current_menu == "build" and build_menu.menu_rect:
                    if build_menu.menu_rect.collidepoint(mx, my):
                        result = build_menu.handle_click((mx, my))

                        if result["type"] == "item":
                            selected_building = result["name"]
                            current_menu = None
                            print(f"Batiment sélectionné : {selected_building}")

                    else:
                        current_menu = None

            camera.handle_event(event)

        build_menu.update(dt, current_menu == "build")

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

        screen.blit(fps_text, (10, 80))
        screen.blit(zoom_text, (10, 100))
        screen.blit(tiles_text, (10, 120))

        if show_hover and 0 <= hover_gx < GRID_WIDTH and 0 <= hover_gy < GRID_HEIGHT:
            hover_text = font.render(
                f"Tile: ({hover_gx}, {hover_gy}) - {terrain[hover_gx][hover_gy]}",
                True,
                (255, 255, 255)
            )
            screen.blit(hover_text, (10, 70))

        hud.draw(
            screen,
            mock_gold,
            mock_population,
            mock_power,
            mock_harmony,
            (mx, my),
            current_menu
        )

        build_menu.draw(screen, (mx, my))

        if selected_building:
            indicator_text = font.render(
                f"Sélectionné : {selected_building}",
                True,
                (255, 255, 255)
            )
            screen.blit(indicator_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
