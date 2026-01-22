from config import TILE_WIDTH, TILE_HEIGHT


def grid_to_iso(gx: int, gy: int, zoom: float = 1.0) -> tuple[int, int]:
    """
    Convert grid coordinates into isometric coordinates
    """
    tw = TILE_WIDTH * zoom
    th = TILE_HEIGHT * zoom

    x = (gx - gy) * (tw / 2)
    y = (gx + gy) * (th / 2)

    return int(x), int(y)


def screen_to_grid(
        screen_x: int,
        screen_y: int,
        camera_offset_x: int,
        camera_offset_y: int,
        zoom: float = 1.0) -> tuple[int, int]:
    """
    Convert screen coordinates to grid coordinates
    """
    x = screen_x - camera_offset_x
    y = screen_y - camera_offset_y

    tw = TILE_WIDTH * zoom
    th = TILE_HEIGHT * zoom

    gx = (y / (th / 2) + x / (tw / 2)) / 2
    gy = (y / (th / 2) - x / (tw / 2)) / 2

    return int(gx), int(gy)
