from __future__ import annotations

# I don't own PowerPoint, so here is the image I used to extract these colors:
# https://www.empowersuite.com/hs-fs/hubfs/Marketing/Blog/Snips/custom-color-palette-powerpoint-master3.png?width=477&name=custom-color-palette-powerpoint-master3.png
BASE_COLORS: list[tuple[int, int, int]] = [(0, 51, 102), (51, 102, 153), (51, 102, 204), (0, 51, 153), (0, 0, 153), (0, 0, 204), (0, 0, 102), (0, 102, 102), (0, 102, 153), (0, 153, 204), (0, 102, 204), (0, 51, 204), (0, 0, 255), (51, 51, 255), (51, 51, 153), (0, 128, 128), (0, 153, 153), (51, 204, 204), (0, 204, 255), (0, 153, 255), (0, 102, 255), (51, 102, 255), (51, 51, 204), (102, 102, 153), (51, 153, 102), (0, 204, 153), (0, 255, 204), (0, 255, 255), (51, 204, 255), (51, 153, 255), (102, 153, 255), (102, 102, 255), (102, 0, 255), (102, 0, 204), (51, 153, 51), (0, 204, 102), (0, 255, 153), (102, 255, 204), (102, 255, 255), (102, 204, 255), (153, 204, 255), (153, 153, 255), (153, 102, 255), (153, 51, 255), (153, 0, 255), (0, 102, 0), (0, 204, 0), (0, 255, 0), (102, 255, 153), (153, 255, 204), (204, 255, 255), (204, 236, 255), (204, 204, 255), (204, 153, 255), (204, 102, 255), (204, 0, 255), (153, 0, 204), (0, 51, 0), (0, 128, 0), (51, 204, 51), (102, 255, 102), (153, 255, 153), (204, 255, 204), (255, 255, 255), (255, 204, 255), (255, 153, 255), (255, 102, 255), (255, 0, 255), (204, 0, 204), (102, 0, 102), (51, 102, 0), (0, 153, 0), (102, 255, 51), (153, 255, 102), (204, 255, 153), (255, 255, 204), (255, 204, 204), (255, 153, 204), (255, 102, 204), (255, 51, 204), (204, 0, 153), (128, 0, 128), (51, 51, 0), (102, 153, 0), (153, 255, 51), (204, 255, 102), (255, 255, 153), (255, 204, 153), (255, 153, 153), (255, 102, 153), (255, 51, 153), (204, 51, 153), (153, 0, 153), (102, 102, 51), (153, 204, 0), (204, 255, 51), (255, 255, 102), (255, 204, 102), (255, 153, 102), (255, 124, 128), (255, 0, 102), (214, 0, 147), (153, 51, 102), (128, 128, 0), (204, 204, 0), (255, 255, 0), (255, 204, 0), (255, 153, 51), (255, 102, 0), (255, 80, 80), (204, 0, 102), (102, 0, 51), (153, 102, 51), (204, 153, 0), (255, 153, 0), (204, 102, 0), (255, 51, 0), (255, 0, 0), (204, 0, 0), (153, 0, 51), (102, 51, 0), (153, 102, 0), (204, 51, 0), (153, 51, 0), (153, 0, 0), (128, 0, 0), (165, 0, 33), (7, 7, 8), (16, 16, 16), (28, 28, 28), (41, 41, 41), (51, 51, 51), (77, 77, 77), (95, 95, 95), (119, 119, 119), (128, 128, 128), (150, 150, 150), (178, 178, 178), (192, 192, 192), (221, 221, 221), (234, 234, 234), (248, 248, 248)]
BASE_OPACITIES: list[float] = [0.05, 0.2, 0.35, 0.5, 0.7, 0.85, 1]

def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return f'#{hex(rgb[0])[2:]}{hex(rgb[1])[2:]}{hex(rgb[2])[2:]}'

class Solution:
    def __init__(self, target: tuple[int, int, int], steps: list[tuple[int, int]]):
        """
        A list of steps to contruct a target color.

        :param steps: A list of steps. Each step should be a tuple with the first item an
        integer to index into the BASE_COLORS array, and the second item an integer to index
        into the BASE_OPACITIES array.
        :type steps: list[tuple[int, int]]
        """
        self.target: tuple[int, int, int] = target
        self.steps: list[tuple[int, int]] = steps

    def __repr__(self):
        return f'Solution(target={self.target}, steps={self.steps})'

    def __str__(self):
        # Target color
        stringified_target: str = f'Target: {rgb_to_hex(self.target)}'

        # Steps
        stringified_steps_list: list[str] = []
        for step in self.steps:
            opacity: float = BASE_OPACITIES[step[1]]
            if opacity == 0:
                stringified_steps_list.append('(0%)')
                continue
            stringified_color: str = rgb_to_hex(BASE_COLORS[step[0]])
            stringified_opacity: str = f'{opacity:.0%}'
            stringified_steps_list.append(f'({stringified_opacity} {stringified_color})')
        stringified_steps: str = f'Steps ({len(self.steps)}): ' + (' '.join(stringified_steps_list))

        # Status and result color
        status: str
        stringified_result: str = 'Result: ERROR'
        try:
            result: tuple[int, int, int] = self.test()
        except ValueError:
            status = 'ERROR'
        else:
            stringified_result = f'Result: {rgb_to_hex(result)}'
            if result == self.target:
                status = 'PASS '
            else:
                status = 'FAIL '

        return f'{status} {stringified_target} {stringified_result} {stringified_steps}'

    def test(self) -> tuple[int, int, int]:
        """
        Tests the solution and returns the actual color produced.

        :return: The actual color produced by the solution.
        :rtype: tuple[int, int, int]
        """
        # Make sure at least one step has 100% opacity so the result is unambiguous
        last_opaque_step: int | None = None
        for i in range(len(self.steps)):
            step: tuple[int, int] = self.steps[i]
            if BASE_OPACITIES[step[1]] == 1:
                last_opaque_step = i
        if last_opaque_step is None:
            raise ValueError('At least one solution step must have 100% opacity to prevent ambiguity regarding the background color')

        # Start from the last opaque step and simulate overlaying the colors
        result: tuple[int, int, int] = BASE_COLORS[self.steps[last_opaque_step][0]]
        for step in self.steps[last_opaque_step+1:]:
            color: tuple[int, int, int] = BASE_COLORS[step[0]]
            opacity: float = BASE_OPACITIES[step[1]]
            result = (
                round(result[0] + opacity * (color[0] - result[0])),
                round(result[1] + opacity * (color[1] - result[1])),
                round(result[2] + opacity * (color[2] - result[2])),
            )

        return result


