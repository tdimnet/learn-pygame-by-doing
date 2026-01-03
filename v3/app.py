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


def draw_items(
        menu_surface: pygame.Surface,
        font: pygame.font.Font,
        items: list,
        offset_x: int) -> dict:
    item_rects = {}
    start_y = 120

    for i, name in enumerate(items):
        tx = 30 + (i % 3) * 90 + offset_x
        ty = start_y + (i // 3) * 90

        rect = pygame.Rect(tx, ty, 64, 64)
        pygame.draw.rect(menu_surface, (80, 160, 80), rect, border_radius=8)

        label = font.render(name, True, WHITE)
        menu_surface.blit(label, (tx, ty + 68))

        item_rects[name] = rect

    return item_rects


def draw_build_menu(
        screen: pygame.Surface,
        font: pygame.font.Font,
        anim_t: float,
        active_category: str,
        previous_category: str,
        category_anim: float):
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

    content_width = MENU_WIDTH
    slide = int(content_width * (1 - category_anim))

    item_buttons = {}
    if category_anim < 1.0:
        if previous_category:
            draw_items(
                menu_surface,
                font,
                BUILD_CATEGORIES[previous_category],
                -slide
            )

        item_buttons = draw_items(
            menu_surface,
            font,
            BUILD_CATEGORIES[active_category],
            content_width - slide
        )
    else:
        item_buttons = draw_items(
            menu_surface,
            font,
            BUILD_CATEGORIES[active_category],
            0
        )

    menu_rect = pygame.Rect(x, y, MENU_WIDTH, MENU_HEIGHT)
    screen.blit(menu_surface, (x, y))

    return (
        {cat: pygame.Rect(x + r.x, y + r.y, r.w, r.h)
        for cat, r in category_rects.items()},
        {name: pygame.Rect(x + r.x, y + r.y, r.w, r.h)
        for name, r in item_buttons.items()},
        menu_rect
    )


def draw_stats_menu(
        screen: pygame.Surface,
        font: pygame.font.Font,
        anim_t: float) -> pygame.Rect:
    x = (SCREEN_WIDTH - MENU_WIDTH) // 2
    y_closed = SCREEN_HEIGHT
    y_open = SCREEN_HEIGHT - MENU_HEIGHT - HUD_HEIGHT - 10

    y = y_closed + (y_open - y_closed) * anim_t
    alpha = int(255 * anim_t)

    menu_surface = pygame.Surface((MENU_WIDTH, MENU_HEIGHT), pygame.SRCALPHA)
    menu_surface.fill((30, 40, 30, alpha))

    title = font.render("Construction", True, WHITE)
    menu_surface.blit(title, (20, 15))

    # Add stuff

    # Tabs
    tabs = ["Population", "Economy", "Resources"]
    cx = 20
    for tab in tabs:
        rect = pygame.Rect(cx, 60, 90, 32)
        pygame.draw.rect(menu_surface, (60, 120, 60), rect, border_radius=6)
        txt = font.render(tab, True, WHITE)
        menu_surface.blit(txt, txt.get_rect(center=rect.center))
        cx += 100

    # Fake stats
    stats = [
        ("Population", "120 (+30)"),
        ("Jobs", "41 / 100"),
        ("Income", "+12 / min"),
        ("Power", "30 / 50"),
    ]

    y_stats = 120
    for label, value in stats:
        txt = font.render(f"{label} : {value}", True, WHITE)
        menu_surface.blit(txt, (30, y_stats))
        y_stats += 40

    menu_rect = pygame.Rect(x, y, MENU_WIDTH, MENU_HEIGHT)
    screen.blit(menu_surface, (x, y))

    return menu_rect


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
        "build": pygame.Rect(SCREEN_WIDTH - 200, hud_rect.y + 12, 48, 40),
        "stats": pygame.Rect(SCREEN_WIDTH - 140, hud_rect.y + 12, 48, 40)
    }


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Buildings")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    menu_rect = None
    menu_anim = 0.0
    menu_anim_speed = 6.0
    current_menu = None

    hud_buttons = None
    menu_buttons, item_buttons = {}, {}
    
    active_category = "Resources"
    previous_category = ""
    category_anim = 1.0
    category_anim_speed = 8.0

    build_mode = False
    selected_building = None

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
                if hud_buttons is not None:
                    if hud_buttons["build"].collidepoint(mouse_pos):
                        current_menu = "build" if current_menu != "build" else None

                    elif hud_buttons["stats"].collidepoint(mouse_pos):
                        current_menu = "stats" if current_menu != "stats" else None

                    elif current_menu and menu_rect and not menu_rect.collidepoint(mouse_pos):
                        # clic hors menu (et pas sur les boutons HUD)
                        if (not hud_buttons["build"].collidepoint(mouse_pos)
                            and not hud_buttons["stats"].collidepoint(mouse_pos)):
                            current_menu = None


                if current_menu and category_anim == 1.0:
                    for cat, rect in menu_buttons.items():
                        if (rect.collidepoint(mouse_pos) and cat !=
                            active_category):
                            previous_category = active_category
                            active_category = cat
                            category_anim = 0.0

                    for name, rect in item_buttons.items():
                        if rect.collidepoint(mouse_pos):
                            build_mode = True
                            selected_building = name
                            current_menu = None


               
        # Idle economy update


        # Draw update
        screen.fill(MAIN_BACKGROUND_COLOR)
        
        for gx in range(GRID_WIDTH):
            for gy in range(GRID_HEIGHT):
                color = (100, 180, 100) if (gx + gy) % 2 == 0 else (80, 160, 80)
                draw_tile(screen, gx, gy, color, offset)


        if current_menu:
            menu_anim = min(1.0, menu_anim + dt * menu_anim_speed)
        else:
            menu_anim = max(0.0, menu_anim - dt * menu_anim_speed)

        if menu_anim > 0:
            if current_menu == "build":
                menu_buttons, item_buttons, menu_rect = draw_build_menu(screen, font, menu_anim,
                                           active_category, previous_category,
                                           category_anim)
            elif current_menu == "stats":
                menu_rect = draw_stats_menu(screen, font, menu_anim)

        if category_anim < 1.0:
            category_anim = min(1.0, category_anim + dt * category_anim_speed)

        if category_anim == 1.0:
            previous_category = ""

        if menu_anim == 0.0:
            menu_rect = None
            menu_buttons.clear()
            item_buttons.clear()


        hud_buttons = draw_hud(screen, font, mouse_pos)

                
        pygame.display.flip()
            
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

