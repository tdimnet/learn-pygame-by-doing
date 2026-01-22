import sys
import pygame

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    GRID_WIDTH, GRID_HEIGHT,
    TILE_WIDTH, TILE_HEIGHT
)
from engine.map_generator import generate_terrain
from engine.game_state import GameState
from engine.milestones import MilestoneSystem
from rendering.camera import Camera
from rendering.tile_renderer import TileRenderer
from rendering.building_renderer import BuildingRenderer
from ui.hud import HUD
from ui.build_menu import BuildMenu
from profiler import Profiler
from ui.debug_overlay import DebugOverlay
from utils.harmony_color import get_harmony_color_bg
from rendering.iso_utils import grid_to_iso 


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Buildings")
    clock = pygame.time.Clock()

    profiler = Profiler(enabled=True)

    print("Génération du terrain...")
    terrain = generate_terrain(GRID_WIDTH, GRID_HEIGHT)
    print(f"Terrain généré : {GRID_WIDTH}x{GRID_HEIGHT}")

    game_state = GameState.load(terrain, "save.json")
   
    camera = Camera(
        initial_offset_x=SCREEN_WIDTH // 2,
        initial_offset_y=SCREEN_HEIGHT // 4
    )

    tile_renderer = TileRenderer()
    building_renderer = BuildingRenderer()

    hud = HUD()
    build_menu = BuildMenu()
    debug_overlay = DebugOverlay()

    milestone_system = MilestoneSystem()

    current_menu = None
    selected_building = None

    pop_effects = [[0.0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    show_grid = True
    show_hover = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mx, my = pygame.mouse.get_pos()

        hover_gx, hover_gy = camera.screen_to_grid(mx, my)

        # Events
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

                if event.key == pygame.K_0:
                    debug_overlay.toggle()
                    print(f"Debug overlay: {'ON' if debug_overlay.enabled else 'OFF'}")

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

                elif selected_building and not current_menu:
                    gx, gy = camera.screen_to_grid(mx, my)

                    if game_state.place_building(gx, gy, selected_building):
                        print(f"Batiment placé : {selected_building} en ({gx} {gy})")
                        pop_effects[gx][gy] = 0.15
                        selected_building = None
                    else:
                        print(f"Impossible de placer {selected_building} ici")

            camera.handle_event(event)

        # Update
        profiler.reset_frame()

        build_menu.update(dt, current_menu == "build")

        with profiler.section("economy"):
            game_state.update(dt)

        with profiler.section("milestones"):
            milestone_system.check(game_state)
            milestone_system.update(dt)

        with profiler.section("pop_effects"):
            for gx in range(GRID_WIDTH):
                for gy in range(GRID_HEIGHT):
                    if pop_effects[gx][gy] > 0:
                        pop_effects[gx][gy] -= dt
                        if pop_effects[gx][gy] < 0:
                            pop_effects[gx][gy] = 0.0
        
        # Render
        bg_color = get_harmony_color_bg(game_state.harmony)
        screen.fill(bg_color)

        with profiler.section("culling"):
            visible_tiles = camera.get_visible_tiles(GRID_WIDTH, GRID_HEIGHT)

        with profiler.section("terrain"):
            tile_renderer.draw_terrain(
                screen,
                game_state.grid.terrain,
                visible_tiles,
                camera.offset_x,
                camera.offset_y,
                camera.zoom,
                show_grid
            )

        with profiler.section("buildings"):
            building_renderer.draw_buildings(
                screen,
                game_state.grid,
                visible_tiles,
                camera.offset_x,
                camera.offset_y,
                camera.zoom,
                pop_effects
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

        if selected_building and 0 <= hover_gx < GRID_WIDTH and 0 <= hover_gy < GRID_HEIGHT:
            if game_state.can_place_building(hover_gx, hover_gy, selected_building):
                outline_color = (100, 255, 100)
            else:
                outline_color = (255, 100, 100)

            iso_x, iso_y = grid_to_iso(hover_gx, hover_gy, camera.zoom)
            cx = iso_x + camera.offset_x
            cy = iso_y + camera.offset_y
            tw = TILE_WIDTH * camera.zoom
            th = TILE_HEIGHT * camera.zoom

            top = (cx, cy - th / 2)
            right = (cx + tw / 2, cy)
            bottom = (cx, cy + th / 2)
            left = (cx - tw / 2, cy)

            pygame.draw.polygon(
                screen,
                outline_color,
                [top, right, bottom, left],
                3
            )

        font = pygame.font.SysFont("arial", 14)

        fps_text = font.render(
            f"FPS: {int(clock.get_fps())}",
            True,
            (255, 255, 255)
        )
        zoom_text = font.render(
            f"Zoom: {camera.zoom:.2f}",
            True,
            (255, 255, 255)
        )
        tiles_text = font.render(
            f"Tiles drawn: {len(visible_tiles)}/{GRID_WIDTH * GRID_HEIGHT}",
            True,
            (255, 255, 255)
        )

        screen.blit(fps_text, (10, 80))
        screen.blit(zoom_text, (10, 100))
        screen.blit(tiles_text, (10, 120))

        if show_hover and 0 <= hover_gx < GRID_WIDTH and 0 <= hover_gy < GRID_HEIGHT:
            hover_text = font.render(
                f"Tile: ({hover_gx}, {hover_gy}) - {game_state.grid.terrain[hover_gx], [hover_gy]}",
                True,
                (255, 255, 255)
            )
            screen.blit(hover_text, (10, 140))


        with profiler.section("ui"):
            hud.draw(
                screen,
                int(game_state.gold),
                int(game_state.population),
                int(game_state.power),
                game_state.harmony,
                (mx, my),
                current_menu
            )
            
            build_menu.draw(screen, (mx, my))

            milestone_system.draw(
                screen,
                pygame.font.SysFont("arial", 22)
            )

            if selected_building:
                indicator_font = pygame.font.SysFont("arial", 16)
                indicator_text = indicator_font.render(
                    f"Sélectionné : {selected_building} (Click pour placer)",
                    True,
                    (255, 255, 100)
                )
                screen.blit(
                    indicator_text,
                    (SCREEN_WIDTH // 2 - 150,
                     SCREEN_HEIGHT - 90)
                )
        
        
        debug_overlay.draw(screen, profiler, game_state)

        pygame.display.flip()
        profiler.end_frame()

    game_state.save("save.json")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
