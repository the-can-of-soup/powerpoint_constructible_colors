from __future__ import annotations

from typing import Callable, Any
from tqdm import tqdm
import common
import random
import time

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
            stringified_target = f'Target: {common.rgb_to_hex(self.target)}'

        # Steps
        stringified_steps_list: list[str] = []
        for step in self.steps:
            opacity: float = common.BASE_OPACITIES[step[1]]
            if opacity == 0:
                stringified_steps_list.append('(0%)')
                continue
            stringified_color: str = common.rgb_to_hex(common.BASE_COLORS[step[0]])
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
            stringified_result = f'Result: {common.rgb_to_hex(result)}'
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
    """
    Bruteforces every combination of up to n layers to find constructible colors.

    :param n: The number of layers.
    :type n: int
    :return: A set of the constructible colors that were found in decimal form.
    :rtype: set[int]
    """
    constructible_colors: set[int] = set()

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
    progress_bar: tqdm = tqdm(desc='Progress     ', total=total_combinations, ascii=(common.PY_IMPLEMENTATION == 'PyPy'))
    constructible_bar: tqdm = tqdm(desc='Constructible', total=(1 << 24), ascii=(common.PY_IMPLEMENTATION == 'PyPy'))

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
            for color in common.COLOR_INDEXES:
                new_steps: list[tuple[int, int]] = steps.copy()
                new_steps.append((color, common.FULLY_OPAQUE_INDEX))
                for_every_solution(step_count - 1, function, new_steps)
        else:
            for color in common.COLOR_INDEXES:
                for opacity in common.OPACITY_INDEXES:
                    new_steps: list[tuple[int, int]] = steps.copy()
                    new_steps.append((color, opacity))
                    for_every_solution(step_count - 1, function, new_steps)

    def add_result_to_constructible_colors(steps: list[tuple[int, int]]) -> None:
        nonlocal constructible_colors

        solution: Solution = Solution(steps)
        initial_length: int = len(constructible_colors)
        constructible_colors.add(common.rgb_to_decimal(solution.test()))
        final_length: int = len(constructible_colors)
        if final_length > initial_length: # Color was added and therefore wasn't in set before
            constructible_bar.update(1)

    for step_count in step_counts:
        for_every_solution(step_count, add_result_to_constructible_colors)
    progress_bar.close()
    constructible_bar.close()

    return constructible_colors

def randomized_search_with_n_layers(n: int = 2, cutoff_time: float = 5.0, known_constructible_colors: set[int] | None = None) -> set[int]:
    """
    Randomly searches for constructible colors by checking combinations of n layers.

    :param n: The number of layers.
    :type n: int
    :param cutoff_time: When this many seconds pass before finding the next unique constructible
    color three consecutive times, the search will end.
    :type cutoff_time: float
    :param known_constructible_colors: Optional set of already known constructible colors in decimal
    form.
    :type known_constructible_colors: set[int]
    :return: A set of the constructible colors that were found in decimal form (including the colors
    from ``known_constructible_colors`` if provided).
    :rtype: set[int]
    """
    constructible_colors: set[int] = set()
    if known_constructible_colors is not None:
        constructible_colors = known_constructible_colors
    constructible_count: int = len(constructible_colors)

    constructible_bar: tqdm = tqdm(desc='Constructible', total=(1 << 24), ascii=(common.PY_IMPLEMENTATION == 'PyPy'))
    constructible_bar.update(constructible_count)

    time_of_last_new_color: float = time.time()
    consecutive_timeouts: int = 0

    while True:
        now: float = time.time()

        test_layers: list[tuple[int, int]] = []
        if n > 0:
            test_layers.append((random.randint(0, len(common.BASE_COLORS) - 1), common.FULLY_OPAQUE_INDEX))
        for _ in range(n - 1):
            test_layers.append((random.randint(0, len(common.BASE_COLORS) - 1), random.randint(0, len(common.BASE_OPACITIES) - 1)))

        solution: Solution = Solution(test_layers)
        constructible_colors.add(common.rgb_to_decimal(solution.test()))

        new_constructible_count: int = len(constructible_colors)
        if new_constructible_count > constructible_count:
            constructible_bar.update(1)
            constructible_count = new_constructible_count
            time_of_last_new_color = now

        if now - time_of_last_new_color >= cutoff_time:
            consecutive_timeouts += 1
            # Only stop after three consecutive timeouts to prevent outliers and things like
            # putting the computer to sleep from instantly stopping the search
            if consecutive_timeouts >= 3:
                constructible_bar.close()
                return constructible_colors
        else:
            consecutive_timeouts = 0

if __name__ == '__main__':
    print('Getting constructible colors...')
    constructible_colors: set[int] = get_constructible_colors_from_n_steps(3)
    print(f'{len(constructible_colors)} / {1 << 24} ({len(constructible_colors) / (1 << 24):.3%}) colors constructible.')
    print(f'{(1 << 24) - len(constructible_colors)} / {1 << 24} ({1 - (len(constructible_colors) / (1 << 24)):.3%}) colors unconstructible.')
