import sys
import pygame

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    GRID_WIDTH, GRID_HEIGHT
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
        

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
