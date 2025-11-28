from __future__ import annotations

from typing import Callable, Any
from tqdm import tqdm # pip install tqdm
import platform
import common

PY_IMPLEMENTATION: str = platform.python_implementation()

def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return f'#{hex(rgb[0])[2:]}{hex(rgb[1])[2:]}{hex(rgb[2])[2:]}'

def rgb_to_decimal(rgb: tuple[int, int, int]) -> int:
    return 65536 * rgb[0] + 256 * rgb[1] + rgb[2]

class Solution:
    def __init__(self, steps: list[tuple[int, int]], target: tuple[int, int, int] | None = None):
        """
        A list of steps to contruct a target color.

        :param steps: A list of steps. Each step should be a tuple with the first item an
        integer to index into the common.BASE_COLORS array, and the second item an integer to index
        into the common.BASE_OPACITIES array.
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
            opacity: float = common.BASE_OPACITIES[step[1]]
            if opacity == 0:
                stringified_steps_list.append('(0%)')
                continue
            stringified_color: str = rgb_to_hex(common.BASE_COLORS[step[0]])
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
            if common.BASE_OPACITIES[step[1]] == 1:
                last_opaque_step = i
        if last_opaque_step is None:
            raise ValueError('At least one solution step must have 100% opacity to prevent ambiguity regarding the background color')

        # Start from the last opaque step and simulate overlaying the colors
        result: tuple[int, int, int] = common.BASE_COLORS[self.steps[last_opaque_step][0]]
        for step in self.steps[last_opaque_step+1:]:
            result = common.apply_layer(result, step)

        return result

def get_constructible_colors_from_n_steps(n: int = 2) -> set[int]:
    constructible_colors: set[int] = set()
    colors_range: range = range(len(common.BASE_COLORS))
    opacities_range: range = range(len(common.BASE_OPACITIES))

    # Find optimal step counts to check to get all possibilities
    # (all numbers from 1 to n, skipping numbers that are factors of larger ones)
    step_counts: list[int] = []
    for step_count in range(1, n + 1):
        should_check: bool = True
        for potential_multiple in range(step_count + 1, n + 1):
            if (potential_multiple % step_count) == 0:
                should_check = False
                break
        if should_check:
            step_counts.append(step_count)

    # Prepare progress bar and constructible colors bar
    total_combinations: float = 0
    for step_count in step_counts:
        partial_combinations: float = (len(common.BASE_COLORS) * len(common.BASE_OPACITIES)) ** (step_count - 1)
        partial_combinations *= len(common.BASE_COLORS)
        total_combinations += partial_combinations
    total_combinations: int = int(total_combinations)
    progress_bar: tqdm = tqdm(desc='Progress     ', total=total_combinations, ascii=(PY_IMPLEMENTATION == 'PyPy'))
    constructible_bar: tqdm = tqdm(desc='Constructible', total=(1 << 24), ascii=(PY_IMPLEMENTATION == 'PyPy'))

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
                new_steps.append((color, common.FULLY_OPAQUE_INDEX))
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
        initial_length: int = len(constructible_colors)
        constructible_colors.add(rgb_to_decimal(solution.test()))
        final_length: int = len(constructible_colors)
        if final_length > initial_length: # Color was added and therefore wasn't in set before
            constructible_bar.update(1)

    for step_count in step_counts:
        for_every_solution(step_count, add_result_to_constructible_colors)
    progress_bar.close()
    constructible_bar.close()

    return constructible_colors

if __name__ == '__main__':
    print('Getting constructible colors...')
    constructible_colors: set[int] = get_constructible_colors_from_n_steps(3)
    print(f'{len(constructible_colors)} / {1 << 24} ({len(constructible_colors) / (1 << 24):.3%}) colors constructible.')
    print(f'{(1 << 24) - len(constructible_colors)} / {1 << 24} ({1 - (len(constructible_colors) / (1 << 24)):.3%}) colors unconstructible.')
