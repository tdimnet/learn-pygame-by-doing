import math


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "FPS Game"

HUD_HEIGHT          = 110
HUD_COLOR           = (20, 20, 20)
HUD_BORDER_COLOR    = (0, 180, 180)
HUD_TEXT_COLOR      = (255, 220, 0)
HUD_LABEL_COLOR     = (160, 160, 160)

FOV = 60
NUM_RAYS = SCREEN_WIDTH
MAX_DEPTH = 20
HALF_FOV = FOV / 2
DELTA_ANGLE = FOV / NUM_RAYS
SCREEN_DIST = SCREEN_WIDTH / (2 * math.tan(math.radians(HALF_FOV)))

PLAYER_SPEED = 3
PLAYER_ROT_SPEED = 2
PLAYER_MAX_HEALTH = 100
PLAYER_START_X = 1.5
PLAYER_START_Y = 1.5
PLAYER_START_ANGLE = 0

ENEMY_SPEED = 1.5
ENEMY_DETECTION_RANGE = 4
ENEMY_ATTACK_RANGE = 2
ENEMY_HEAlTH = 100
ENEMY_DAMAGE = 10
ENEMY_ATTACK_COOLDOWN = 1.5

WEAPONS = {
    "pistol": {
        "damage": 30,
        "cooldown": 0.5,
        "frame_count": 5,
        "frame_speed": 0.1
    },
    "rifle": {
        "damage": 50,
        "cooldown": 0.3,
        "frame_count": 5,
        "frame_speed": 0.08
    }
}
WEAPON_FRAME_W = 64
WEAPON_FRAME_H = 64
WEAPON_SCALE = 6
WEAPON_ROW = {
    "knife": 1,
    "pistol": 1,
    "rifle": 2
}
WEAPONS_SHEET = "assets/sprites/weapons/fps_weapons.png"

FLOOR_COLOR = (70, 70, 70)
CEILING_COLOR = (40, 40, 40)

TEXTURES_PATH = "assets/textures/"
SPRITES_PATH = "assets/sprites/"
SOUNDS_PATH = "assets/sounds/"

WALL_TEXTURES = {
    1: "stone_01.png",
    2: "stone_02.png",
    3: "stone_03.png",
    4: "stone_04.png",
    5: "stone_05.png",
}

TILE_SIZE = 64
EMPTY = 0
WALL = 1
DOOR = 4

LANGUAGES = {
    "fr": {
        "menu_play": "Jouer",
        "menu_quit": "Quitter",
        "menu_settings": "Options",
        "menu_language": "Langue"
    },
    "en": {
        "menu_play": "Play",
        "menu_quit": "Quit",
        "menu_settings": "Settings",
        "menu_language": "Language"
    }
}

CURRENT_LANG = "fr"

def t(key: str) -> str:
    return LANGUAGES[CURRENT_LANG].get(key, key)
