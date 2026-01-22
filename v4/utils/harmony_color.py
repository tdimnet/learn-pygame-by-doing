from config import (
    BASE_BG_COLOR,
    WARM_BG_COLOR,
    COLD_BG_COLOR
)


def get_harmony_color_bg(harmony: float) -> tuple[int, int, int]:
    h = max(0, min(100, harmony)) / 100.0

    if h >= 0.5:
        t = (h - 0.5) * 2
        return (
            int(BASE_BG_COLOR[0] + t * (WARM_BG_COLOR[0] - BASE_BG_COLOR[0])),
            int(BASE_BG_COLOR[1] + t * (WARM_BG_COLOR[1] - BASE_BG_COLOR[1])),
            int(BASE_BG_COLOR[2] + t * (WARM_BG_COLOR[2] - BASE_BG_COLOR[2])),
        )

    else:
        t = (0.5 - h) * 2
        return (
            int(BASE_BG_COLOR[0] + t * (COLD_BG_COLOR[0] - BASE_BG_COLOR[0])),
            int(BASE_BG_COLOR[1] + t * (COLD_BG_COLOR[1] - BASE_BG_COLOR[1])),
            int(BASE_BG_COLOR[2] + t * (COLD_BG_COLOR[2] - BASE_BG_COLOR[2])),
        )
