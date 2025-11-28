from __future__ import annotations

from typing import Callable, Any
from tqdm import tqdm # pip install tqdm

# I don't own PowerPoint, so here is the image I used to extract these colors:
# https://www.empowersuite.com/hs-fs/hubfs/Marketing/Blog/Snips/custom-color-palette-powerpoint-master3.png?width=477&name=custom-color-palette-powerpoint-master3.png
BASE_COLORS: list[tuple[int, int, int]] = [(0, 51, 102), (51, 102, 153), (51, 102, 204), (0, 51, 153), (0, 0, 153), (0, 0, 204), (0, 0, 102), (0, 102, 102), (0, 102, 153), (0, 153, 204), (0, 102, 204), (0, 51, 204), (0, 0, 255), (51, 51, 255), (51, 51, 153), (0, 128, 128), (0, 153, 153), (51, 204, 204), (0, 204, 255), (0, 153, 255), (0, 102, 255), (51, 102, 255), (51, 51, 204), (102, 102, 153), (51, 153, 102), (0, 204, 153), (0, 255, 204), (0, 255, 255), (51, 204, 255), (51, 153, 255), (102, 153, 255), (102, 102, 255), (102, 0, 255), (102, 0, 204), (51, 153, 51), (0, 204, 102), (0, 255, 153), (102, 255, 204), (102, 255, 255), (102, 204, 255), (153, 204, 255), (153, 153, 255), (153, 102, 255), (153, 51, 255), (153, 0, 255), (0, 102, 0), (0, 204, 0), (0, 255, 0), (102, 255, 153), (153, 255, 204), (204, 255, 255), (204, 236, 255), (204, 204, 255), (204, 153, 255), (204, 102, 255), (204, 0, 255), (153, 0, 204), (0, 51, 0), (0, 128, 0), (51, 204, 51), (102, 255, 102), (153, 255, 153), (204, 255, 204), (255, 255, 255), (255, 204, 255), (255, 153, 255), (255, 102, 255), (255, 0, 255), (204, 0, 204), (102, 0, 102), (51, 102, 0), (0, 153, 0), (102, 255, 51), (153, 255, 102), (204, 255, 153), (255, 255, 204), (255, 204, 204), (255, 153, 204), (255, 102, 204), (255, 51, 204), (204, 0, 153), (128, 0, 128), (51, 51, 0), (102, 153, 0), (153, 255, 51), (204, 255, 102), (255, 255, 153), (255, 204, 153), (255, 153, 153), (255, 102, 153), (255, 51, 153), (204, 51, 153), (153, 0, 153), (102, 102, 51), (153, 204, 0), (204, 255, 51), (255, 255, 102), (255, 204, 102), (255, 153, 102), (255, 124, 128), (255, 0, 102), (214, 0, 147), (153, 51, 102), (128, 128, 0), (204, 204, 0), (255, 255, 0), (255, 204, 0), (255, 153, 51), (255, 102, 0), (255, 80, 80), (204, 0, 102), (102, 0, 51), (153, 102, 51), (204, 153, 0), (255, 153, 0), (204, 102, 0), (255, 51, 0), (255, 0, 0), (204, 0, 0), (153, 0, 51), (102, 51, 0), (153, 102, 0), (204, 51, 0), (153, 51, 0), (153, 0, 0), (128, 0, 0), (165, 0, 33), (7, 7, 8), (16, 16, 16), (28, 28, 28), (41, 41, 41), (51, 51, 51), (77, 77, 77), (95, 95, 95), (119, 119, 119), (128, 128, 128), (150, 150, 150), (178, 178, 178), (192, 192, 192), (221, 221, 221), (234, 234, 234), (248, 248, 248)]
BASE_OPACITIES: list[float] = [0.05, 0.2, 0.35, 0.5, 0.7, 0.85, 1]
FULLY_OPAQUE_INDEX: int = 6

def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return f'#{hex(rgb[0])[2:]}{hex(rgb[1])[2:]}{hex(rgb[2])[2:]}'

def rgb_to_decimal(rgb: tuple[int, int, int]) -> int:
    return 65536 * rgb[0] + 256 * rgb[1] + rgb[2]

class Solution:
    def __init__(self, steps: list[tuple[int, int]], target: tuple[int, int, int] | None = None):
        """
        A list of steps to contruct a target color.

        :param steps: A list of steps. Each step should be a tuple with the first item an
        integer to index into the BASE_COLORS array, and the second item an integer to index
        into the BASE_OPACITIES array.
        :type steps: list[tuple[int, int]]
        :param target: An optional target color.
        :type target: tuple[int, int, int]
        """
        self.target: tuple[int, int, int] | None = target
        self.steps: list[tuple[int, int]] = steps

    def __repr__(self):
        return f'Solution(target={self.target}, steps={self.steps})'

    def __str__(self):
        # Target color
        stringified_target: str = 'Target: NONE'
        if self.target is not None:
            stringified_target = f'Target: {rgb_to_hex(self.target)}'

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
            # PowerPoint appears to round color channels to the nearest integer at every step using banker's rounding (?).
            # TODO: Figure out why these examples in PowerPoint cause weird results in the web version:
            # - 50% opacity #fefefe on top of 100% opacity #ffffff; expected: #fefefe, actual: #fefefe (checks out)
            # - 50% opacity #ffffff on top of 100% opacity #fefefe; expected: #fefefe, actual: #ffffff (what the f-string)
            # - 1% opacity #d4d4d4 (stacked a whole bunch) on top of 100% opacity #ffffff; expected: something close to #d4d4d4, actual: #dcdcdc (checks out)
            # - 1% opacity #d5d5d5 (stacked a whole bunch) on top of 100% opacity #ffffff; expected: something close to #d5d5d5, actual: #ffffff (????)
            result = (
                round(result[0] + opacity * (color[0] - result[0])),
                round(result[1] + opacity * (color[1] - result[1])),
                round(result[2] + opacity * (color[2] - result[2])),
            )

        return result

def get_constructible_colors_from_n_steps(n: int = 2) -> set[int]:
    constructible_colors: set[int] = set()
    colors_range: range = range(len(BASE_COLORS))
    opacities_range: range = range(len(BASE_OPACITIES))

    total_combinations: float = 0
    for step_count in range(1, n + 1):
        partial_combinations: float = (len(BASE_COLORS) * len(BASE_OPACITIES)) ** (step_count - 1)
        partial_combinations *= len(BASE_COLORS)
        total_combinations += partial_combinations
    total_combinations: int = int(total_combinations)
    progress_bar: tqdm = tqdm(total=total_combinations)

    def for_every_solution(step_count: int, function: Callable[[list[tuple[int, int]]], Any], steps: list[tuple[int, int]] | None = None) -> None:
        if steps is None:
            steps = []
        if step_count < 1:
            progress_bar.update(1)

            reversed_steps: list[tuple[int, int]] = steps.copy()
            reversed_steps.reverse()
            function(reversed_steps)
            return
        if step_count == 1:
            for color in colors_range:
                new_steps: list[tuple[int, int]] = steps.copy()
                new_steps.append((color, FULLY_OPAQUE_INDEX))
                for_every_solution(step_count - 1, function, new_steps)
        else:
            for color in colors_range:
                for opacity in opacities_range:
                    new_steps: list[tuple[int, int]] = steps.copy()
                    new_steps.append((color, opacity))
                    for_every_solution(step_count - 1, function, new_steps)

    def add_result_to_constructible_colors(steps: list[tuple[int, int]]) -> None:
        nonlocal constructible_colors

        solution: Solution = Solution(steps)
        constructible_colors.add(rgb_to_decimal(solution.test()))

    for step_count in range(1, n + 1):
        for_every_solution(step_count, add_result_to_constructible_colors)
    progress_bar.close()

    return constructible_colors

if __name__ == '__main__':
    print('Getting constructible colors...')
    constructible_colors: set[int] = get_constructible_colors_from_n_steps(3)
    print(f'{len(constructible_colors)} / {1 << 24} ({len(constructible_colors) / (1 << 24):.3%}) colors constructible.')
    print(f'{(1 << 24) - len(constructible_colors)} / {1 << 24} ({1 - (len(constructible_colors) / (1 << 24)):.3%}) colors unconstructible.')
