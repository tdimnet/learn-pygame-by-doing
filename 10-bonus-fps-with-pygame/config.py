import math


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "FPS Game"

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
ENEMY_DETECTION_RANGE = 10
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

FLOOR_COLOR = (70, 70, 70)
CEILING_COLOR = (40, 40, 40)

TILE_SIZE = 64
EMPTY = 0
WALL = 1
DOOR = 4

LANGUAGES = {
    "fr": {},
    "en": {}
}

CURRENT_LANG = "fr"

def t(key: str) -> str:
    return LANGUAGES[CURRENT_LANG].get(key, key)
