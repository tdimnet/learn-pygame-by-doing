import sys
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

TILE_WIDTH = 64
TILE_HEIGHT = 32

GRID_WIDTH = 10
GRID_HEIGHT= 10

HUD_HEIGHT = 64

MENU_WIDTH = 320
MENU_HEIGHT = 360

MAIN_BACKGROUND_COLOR = (34, 139, 34)
TILE_BACKGROUND_COLOR = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BUILD_CATEGORIES = {
    "Resources": ["Farm", "Lumber", "Mine", "Water", "Power"],
    "Services": ["House", "School", "Hospital"],
    "Decoration": ["Tree", "Park", "Statue"]
}


def grid_to_iso(gx: int, gy: int) -> tuple[int, int]:
    x = (gx - gy) * (TILE_WIDTH // 2)
    y = (gx + gy) * (TILE_HEIGHT // 2)
    return x, y


def draw_tile(
        surface: pygame.Surface,
        gx: int,
        gy: int,
        color: tuple[int, int, int],
        offset: tuple[int, int]) -> None:
    iso_x, iso_y = grid_to_iso(gx, gy)
    offset_x, offset_y = offset
    cx = iso_x + offset_x
    cy = iso_y + offset_y

    top = (cx, cy - TILE_HEIGHT // 2)
    right = (cx + TILE_WIDTH // 2, cy)
    bottom = (cx, cy + TILE_HEIGHT // 2)
    left = (cx - TILE_WIDTH // 2, cy)
    
    pygame.draw.polygon(
        surface,
        color,
        [top, right, bottom, left])
    pygame.draw.polygon(
        surface,
        BLACK,
        [top, right, bottom, left],
        1)


def draw_build_menu(
        screen: pygame.Surface,
        font: pygame.font.Font,
        anim_t: float,
        active_category: str,
        mouse_pos: tuple[int, int]) -> dict:
    x = (SCREEN_WIDTH - MENU_WIDTH) // 2
    y_closed = SCREEN_HEIGHT
    y_open = SCREEN_HEIGHT - MENU_HEIGHT - HUD_HEIGHT - 10

    y = y_closed + (y_open - y_closed) * anim_t
    alpha = int(255 * anim_t)

    menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT), pygame.SRCALPHA)
    menu_surface.fill((30, 40, 30, alpha))

    title = font.render("Construction", True, WHITE)
    menu_surface.blit(title, (20, 15))

    category_rects = {}
    cx = 20
    for cat in BUILD_CATEGORIES.keys():
        rect = pygame.Rect(cx, 60, 90, 32)
        category_rects[cat] = rect

        color = (90, 160, 90) if cat == active_category else (60, 120, 60)
        pygame.draw.rect(menu_surface, color, rect, border_radius=6)

        txt = font.render(cat, True, WHITE)
        menu_surface.blit(txt, txt.get_rect(center=rect.center))
        cx += 100

    items = BUILD_CATEGORIES[active_category]
    start_y = 120

    for i, name in enumerate(items):
        tx = 30 + (i % 3) * 90
        ty = start_y + (i // 3) * 90

        tile_rect = pygame.Rect(tx, ty, 64, 64)
        pygame.draw.rect(menu_surface, (80, 160, 80), tile_rect,
                         border_radius=8)

        label = font.render(name, True, WHITE)
        menu_surface.blit(label, (tx, ty + 68))


    screen.blit(menu_surface, (x, y))

    return {
        cat: pygame.Rect(x + r.x, y + r.y, r.w, r.h)
        for cat, r in category_rects.items()
    }


def draw_hud(
        screen: pygame.Surface,
        font: pygame.font.Font,
        mouse_pos: tuple[int, int]) -> dict:
    hud_rect = pygame.Rect(
        0,
        SCREEN_HEIGHT - HUD_HEIGHT,
        SCREEN_WIDTH,
        HUD_HEIGHT
    )

    hud_surface = pygame.Surface((SCREEN_WIDTH, HUD_HEIGHT), pygame.SRCALPHA)
    hud_surface.fill((20, 30, 20, 210))
    screen.blit(hud_surface, hud_rect.topleft)

    resources = [
        ("g", "5000"),
        ("p", "120"),
        ("e", "30"),
    ]

    x = 20
    for icon, value in resources:
        text = font.render(f"{icon} {value}", True, WHITE)
        screen.blit(text, (x, hud_rect.y + 20))
        x += 120

    buttons = [
        ("Build", SCREEN_WIDTH - 200),
        ("Stats", SCREEN_WIDTH - 140),
        ("Sets", SCREEN_WIDTH - 80)
    ]

    for label, x in buttons:
        rect = pygame.Rect(x, hud_rect.y + 12, 48, 40)

        color = (60, 120, 60)
        if rect.collidepoint(mouse_pos):
            color = (90, 160, 90)

        pygame.draw.rect(screen, color, rect, border_radius=8)

        txt = font.render(label, True, WHITE)
        txt_rect = txt.get_rect(center=rect.center)
        screen.blit(txt, txt_rect)

    return {
        "build": pygame.Rect(SCREEN_WIDTH - 200, hud_rect.y + 12, 48, 40)
    }


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Buildings")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    menu_open = False
    menu_anim = 0.0
    menu_anim_speed = 6.0

    hud_buttons = None
    menu_buttons = {}
    active_category = "Resources"

    offset = (
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 4
    )

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if (hud_buttons is not None and
                    hud_buttons["build"].collidepoint(mouse_pos)):
                        menu_open = not menu_open

                if menu_open:
                    for cat, rect in menu_buttons.items():
                        if rect.collidepoint(mouse_pos):
                            active_category = cat

               
        # Idle economy update


        # Draw update
        screen.fill(MAIN_BACKGROUND_COLOR)
        
        for gx in range(GRID_WIDTH):
            for gy in range(GRID_HEIGHT):
                color = (100, 180, 100) if (gx + gy) % 2 == 0 else (80, 160, 80)
                draw_tile(screen, gx, gy, color, offset)


        if menu_open:
            menu_anim = min(1.0, menu_anim + dt * menu_anim_speed)
        else:
            menu_anim = max(0.0, menu_anim - dt * menu_anim_speed)

        if menu_anim > 0:
            menu_buttons = draw_build_menu(screen, font, menu_anim, active_category, mouse_pos)


        hud_buttons = draw_hud(screen, font, mouse_pos)

                
        pygame.display.flip()
            
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

