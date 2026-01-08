SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

TILE_WIDTH = 64
TILE_HEIGHT = 32

GRID_WIDTH = 50
GRID_HEIGHT = 50

ZOOM_MIN = 0.5
ZOOM_MAX = 2.0
ZOOM_STEP = 0.1

# Background colors (harmony system)
BASE_BG_COLOR = (60, 120, 180)
WARM_BG_COLOR = (70, 140, 160)
COLD_BG_COLOR = (50, 100, 160)

# Terrain colors
COLOR_GRASS = (100, 180, 100)
COLOR_GRASS_ALT = (80, 160, 80)
COLOR_WATER = (54, 117, 136)
COLOR_SAND = (210, 180, 140)
COLOR_FOREST = (1, 50, 32)
COLOR_MOUNTAIN = (100, 65, 23)

# UI colors
COLOR_UI_BG = (30, 30, 30)
COLOR_UI_TEXT = (255, 255, 255)
COLOR_BUTTON_NORMAL = (60, 120, 60)
COLOR_BUTTON_HOVER = (90, 160, 90)
COLOR_BUTTON_SELECTED = (120, 200, 120)

# Building colors
COLOR_BUILDING_HOUSE = (50, 150, 255)
COLOR_BUILDING_FACTORY = (200, 60, 60)
COLOR_BUILDING_POWERPLANT = (230, 200, 60)
COLOR_BUILDING_GARDEN = (80, 180, 120)
COLOR_BUILDING_PARK = (60, 160, 100)

BUILDINGS = {
    "house": {
        "cost": 10,
        "pop_production": 1,
        "gold_production": 0,
        "power_production": 0,
        "pop_consume": 0,
        "color": COLOR_BUILDING_HOUSE,
        "category": "Résidentiel"
    },
    "factory": {
        "cost": 20,
        "pop_production": 0,
        "gold_production": 2,
        "power_production": 0,
        "pop_consume": 1,
        "color": COLOR_BUILDING_FACTORY,
        "category": "Industrie"
    },
    "powerplant": {
        "cost": 50,
        "pop_production": 0,
        "gold_production": 0,
        "power_production": 1,
        "pop_consume": 1,
        "color": COLOR_BUILDING_POWERPLANT,
        "category": "Industrie"
    },
    "garden": {
        "cost": 30,
        "pop_production": 1,
        "gold_production": 0,
        "power_production": 0,
        "pop_consume": 0,
        "color": COLOR_BUILDING_GARDEN,
        "category": "Résidentiel"
    },
    "park": {
        "cost": 80,
        "pop_production": 1,
        "gold_production": 0,
        "power_production": 0,
        "pop_consume": 0,
        "color": COLOR_BUILDING_PARK,
        "category": "Résidentiel"
    }
}

BUILD_CATEGORIES = {
    "Résidentiel": ["house", "garden", "park"],
    "Industrie": ["factory", "powerplant"]
}

# Map generation

