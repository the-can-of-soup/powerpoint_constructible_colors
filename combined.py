from __future__ import annotations

from tqdm import tqdm
import bruteforcer
import search
import common

BRUTE_FORCE_DEPTH: int = 3
RANDOM_SEARCH_DEPTH: int = 5
RANDOM_SEARCH_CUTOFF_TIME: float = 5.0

if __name__ == '__main__':
    constructible_count: int = 0

    print(f'Brute forcing every combination of up to {BRUTE_FORCE_DEPTH} layers...')
    constructible_colors: set[int] = bruteforcer.get_constructible_colors_from_n_steps(BRUTE_FORCE_DEPTH)
    constructible_count += len(constructible_colors)

    print('')
    print(f'Randomly checking combinations of {RANDOM_SEARCH_DEPTH} layers...')
    constructible_colors = bruteforcer.randomized_search_with_n_layers(
        n=RANDOM_SEARCH_DEPTH,
        cutoff_time=RANDOM_SEARCH_CUTOFF_TIME,
        known_constructible_colors=constructible_colors,
    )
    constructible_count = len(constructible_colors)

    print('')
    print('Searching remaining colors...')
    remaining_color_count: int = (1 << 24) - constructible_count
    progress_bar: tqdm = tqdm(desc='Progress     ', total=remaining_color_count, ascii=(common.PY_IMPLEMENTATION == 'PyPy'))
    constructible_bar: tqdm = tqdm(desc='Constructible', total=(1 << 24), ascii=(common.PY_IMPLEMENTATION == 'PyPy'))
    unconstructible_bar: tqdm = tqdm(desc='Unconstruct. ', total=(1 << 24), ascii=(common.PY_IMPLEMENTATION == 'PyPy'))
    constructible_bar.update(constructible_count)
    unconstructible_bar.update((1 << 24) - constructible_count)

    for r in range(256):
        for g in range(256):
            for b in range(256):
                if (r, g, b) in constructible_colors:
                    continue
                solver_result: list[search.SearchNode] | None = search.solve((r, g, b))
                progress_bar.update(1)
                if solver_result is None:
                    unconstructible_bar.update(1)
                else:
                    constructible_bar.update(1)
                    constructible_count += 1

    print(f'{constructible_count} / {1 << 24} ({constructible_count / (1 << 24):.3%}) colors constructible.')
    print(f'{(1 << 24) - constructible_count} / {1 << 24} ({1 - (constructible_count / (1 << 24)):.3%}) colors unconstructible.')

    print('')
    input('Press ENTER to close.')
