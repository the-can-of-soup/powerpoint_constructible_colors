from __future__ import annotations

import platform

# I don't own PowerPoint, so here is the image I used to extract these colors:
# https://www.empowersuite.com/hs-fs/hubfs/Marketing/Blog/Snips/custom-color-palette-powerpoint-master3.png?width=477&name=custom-color-palette-powerpoint-master3.png
BASE_COLORS: list[tuple[int, int, int]] = [(0, 51, 102), (51, 102, 153), (51, 102, 204), (0, 51, 153), (0, 0, 153), (0, 0, 204), (0, 0, 102), (0, 102, 102), (0, 102, 153), (0, 153, 204), (0, 102, 204), (0, 51, 204), (0, 0, 255), (51, 51, 255), (51, 51, 153), (0, 128, 128), (0, 153, 153), (51, 204, 204), (0, 204, 255), (0, 153, 255), (0, 102, 255), (51, 102, 255), (51, 51, 204), (102, 102, 153), (51, 153, 102), (0, 204, 153), (0, 255, 204), (0, 255, 255), (51, 204, 255), (51, 153, 255), (102, 153, 255), (102, 102, 255), (102, 0, 255), (102, 0, 204), (51, 153, 51), (0, 204, 102), (0, 255, 153), (102, 255, 204), (102, 255, 255), (102, 204, 255), (153, 204, 255), (153, 153, 255), (153, 102, 255), (153, 51, 255), (153, 0, 255), (0, 102, 0), (0, 204, 0), (0, 255, 0), (102, 255, 153), (153, 255, 204), (204, 255, 255), (204, 236, 255), (204, 204, 255), (204, 153, 255), (204, 102, 255), (204, 0, 255), (153, 0, 204), (0, 51, 0), (0, 128, 0), (51, 204, 51), (102, 255, 102), (153, 255, 153), (204, 255, 204), (255, 255, 255), (255, 204, 255), (255, 153, 255), (255, 102, 255), (255, 0, 255), (204, 0, 204), (102, 0, 102), (51, 102, 0), (0, 153, 0), (102, 255, 51), (153, 255, 102), (204, 255, 153), (255, 255, 204), (255, 204, 204), (255, 153, 204), (255, 102, 204), (255, 51, 204), (204, 0, 153), (128, 0, 128), (51, 51, 0), (102, 153, 0), (153, 255, 51), (204, 255, 102), (255, 255, 153), (255, 204, 153), (255, 153, 153), (255, 102, 153), (255, 51, 153), (204, 51, 153), (153, 0, 153), (102, 102, 51), (153, 204, 0), (204, 255, 51), (255, 255, 102), (255, 204, 102), (255, 153, 102), (255, 124, 128), (255, 0, 102), (214, 0, 147), (153, 51, 102), (128, 128, 0), (204, 204, 0), (255, 255, 0), (255, 204, 0), (255, 153, 51), (255, 102, 0), (255, 80, 80), (204, 0, 102), (102, 0, 51), (153, 102, 51), (204, 153, 0), (255, 153, 0), (204, 102, 0), (255, 51, 0), (255, 0, 0), (204, 0, 0), (153, 0, 51), (102, 51, 0), (153, 102, 0), (204, 51, 0), (153, 51, 0), (153, 0, 0), (128, 0, 0), (165, 0, 33), (7, 7, 8), (16, 16, 16), (28, 28, 28), (41, 41, 41), (51, 51, 51), (77, 77, 77), (95, 95, 95), (119, 119, 119), (128, 128, 128), (150, 150, 150), (178, 178, 178), (192, 192, 192), (221, 221, 221), (234, 234, 234), (248, 248, 248), (0, 0, 0)]
COLOR_INDEXES: list[int] = list(range(len(BASE_COLORS)))

BASE_OPACITIES: list[float] = [0.05, 0.2, 0.35, 0.5, 0.7, 0.85, 1]
OPACITY_INDEXES: list[int] = list(range(len(BASE_OPACITIES)))
FULLY_OPAQUE_INDEX: int = BASE_OPACITIES.index(1)

CONSTRUCTIBLE_COLORS_FILE_PATH: str = 'constructible_colors.dat'

PY_IMPLEMENTATION: str = platform.python_implementation()



def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return f'#{hex(rgb[0])[2:]:02}{hex(rgb[1])[2:]:02}{hex(rgb[2])[2:]:02}'

def rgb_to_decimal(rgb: tuple[int, int, int]) -> int:
    return (rgb[0] << 16) | (rgb[1] << 8) | rgb[2]

def rgb_to_bytes(rgb: tuple[int, int, int]) -> bytes:
    return rgb[0].to_bytes() + rgb[1].to_bytes() + rgb[2].to_bytes()

def decimal_to_rgb(decimal: int) -> tuple[int, int, int]:
    return (
        (decimal >> 16) & 255,
        (decimal >> 8) & 255,
        decimal & 255,
    )

def bytes_to_rgb(data: bytes) -> tuple[int, int, int]:
    return data[0], data[1], data[2]

def apply_layer(old_rgb: tuple[int, int, int] | None, layer: tuple[int, int]) -> tuple[int, int, int] | None:
    """
    Applies a layer to a color.

    :param old_rgb: The color the layer is being applied to, or None if dependent on the background color.
    :type old_rgb: tuple[int, int, int] | None
    :param layer: The layer to apply to the color as a tuple of two indexes. The first index is for the
    BASE_COLORS list, and the other is for the BASE_OPACITIES list.
    :type layer: tuple[int, int]
    :return: The resulting color, or None if dependent on the background color.
    :rtype: tuple[int, int, int] | None
    """
    layer_color: tuple[int, int, int] = BASE_COLORS[layer[0]]
    layer_opacity: float = BASE_OPACITIES[layer[1]]

    if old_rgb is None:
        if layer_opacity == 1:
            return layer_color
        return None

    # PowerPoint appears to round color channels to the nearest integer at every step using banker's rounding (?).
    # TODO: Figure out why these examples in PowerPoint cause weird results in the web version:
    # - 50% opacity #fefefe on top of 100% opacity #ffffff; expected: #fefefe, actual: #fefefe (checks out)
    # - 50% opacity #ffffff on top of 100% opacity #fefefe; expected: #fefefe, actual: #ffffff (what the f-string)
    # - 1% opacity #d4d4d4 (stacked a whole bunch) on top of 100% opacity #ffffff; expected: something close to #d4d4d4, actual: #dcdcdc (checks out)
    # - 1% opacity #d5d5d5 (stacked a whole bunch) on top of 100% opacity #ffffff; expected: something close to #d5d5d5, actual: #ffffff, but only in Firefox (????)
    result: tuple[int, int, int] = (
        round(old_rgb[0] + layer_opacity * (layer_color[0] - old_rgb[0])),
        round(old_rgb[1] + layer_opacity * (layer_color[1] - old_rgb[1])),
        round(old_rgb[2] + layer_opacity * (layer_color[2] - old_rgb[2])),
    )

    return result
