from __future__ import annotations

from astar import AStar
from tqdm import tqdm
import common
import math

class SearchNode:
    def __init__(self, rgb: tuple[int, int, int] | None, top_layer: tuple[int, int] | None = None):
        """
        An RGB color and the final layer used to create the color.

        :param rgb: The color, or None if dependent on the background color.
        :type rgb: tuple[int, int, int] | None
        :param top_layer: The final layer to create this color, or None if this is the start color.
        The layer is a tuple of two indexes. The first index is for the common.BASE_COLORS list, and
        the other is for the common.BASE_OPACITIES list.
        """
        self.rgb: tuple[int, int, int] | None = rgb
        self.top_layer: tuple[int, int] | None = top_layer

    def __hash__(self) -> int:
        return hash(self.rgb)

    def __eq__(self, other: SearchNode) -> bool:
        return self.rgb == other.rgb

    def __repr__(self) -> str:
        return f'SearchNode(rgb={self.rgb}, top_layer={self.top_layer})'

    def __str__(self) -> str:
        result: str = ''
        if self.top_layer is None:
            result += '(START)'
        else:
            result += f'({common.BASE_OPACITIES[self.top_layer[1]]:.0%}'
            result += f' {common.rgb_to_hex(common.BASE_COLORS[self.top_layer[0]])})'
        if self.rgb is None:
            result += '->AMBIGUOUS'
        else:
            result += f'->{common.rgb_to_hex(self.rgb)}'
        return result

class ColorsSearch(AStar):
    def neighbors(self, node: SearchNode) -> set[SearchNode]:
        # Gets the possible next nodes for a given node

        neighbors: set[SearchNode] = set()

        opacity_indexes: list[int] = common.OPACITY_INDEXES
        if node.rgb is None:
            # Always apply an opaque layer if one hasn't been applied yet
            opacity_indexes = [common.FULLY_OPAQUE_INDEX]

        for opacity_index in opacity_indexes:
            for color_index in common.COLOR_INDEXES:
                layer: tuple[int, int] = (color_index, opacity_index)
                rgb: tuple[int, int, int] | None = common.apply_layer(node.rgb, layer)
                neighbor: SearchNode = SearchNode(rgb=rgb, top_layer=layer)
                neighbors.add(neighbor)

        return neighbors

    def distance_between(self, node1: SearchNode, node2: SearchNode) -> float:
        # Gets the cost between two ADJACENT nodes

        if node1.rgb is not None and node2.rgb is None:
            # Never go from an unambiguous node to an ambiguous one
            return math.inf

        # All other moves cost the same
        return 1

    def heuristic_cost_estimate(self, current_node: SearchNode, goal_node: SearchNode) -> float:
        # ESTIMATES the cost between a node and the goal node

        if current_node.rgb is None or goal_node.rgb is None:
            # The estimated cost between an ambiguous node and any other node is infinite
            return math.inf

        # Use Euclidean distance between RGB values
        return math.hypot(
            goal_node.rgb[0] - current_node.rgb[0],
            goal_node.rgb[1] - current_node.rgb[1],
            goal_node.rgb[2] - current_node.rgb[2],
        )

    def is_goal_reached(self, current_node: SearchNode, goal_node: SearchNode) -> bool:
        # Returns True if the goal is reached

        return current_node == goal_node

def solve(target_rgb: tuple[int, int, int]) -> list[SearchNode] | None:
    """
    Finds the optimal path of nodes to reach a target color.

    :param target_rgb: The target color.
    :type target_rgb: tuple[int, int, int]
    :return: A list of nodes, or None if the color is unconstructible.
    :rtype: list[SearchNode] | None
    """
    solver: ColorsSearch = ColorsSearch()
    start_node: SearchNode = SearchNode(rgb=None)
    goal_node: SearchNode = SearchNode(rgb=target_rgb)
    solver_result = solver.astar(start_node, goal_node)
    if solver_result is None:
        return None
    return list(solver_result)

def format_solver_result(solver_result: list[SearchNode] | None, target_rgb: tuple[int, int, int]) -> str:
    """
    Formats the result from ``solve()``.

    :param solver_result: The result from ``solve()``.
    :type solver_result: list[SearchNode] | None
    :param target_rgb: The target color.
    :type target_rgb: tuple[int, int, int]
    :return: The formatted result.
    :rtype: str
    """
    if solver_result is None:
        return f'FAIL | Target: {common.rgb_to_hex(target_rgb)}'

    steps: list[SearchNode] = solver_result[1:]
    formatted_steps: str = ', '.join([str(node) for node in steps])
    word_layers: str = 'layer' if len(steps) == 1 else 'layers'
    return f'PASS | Target: {common.rgb_to_hex(target_rgb)} | {len(steps)} {word_layers}: {formatted_steps}'

if __name__ == '__main__':
    print('Getting constructible colors...')
    progress_bar: tqdm = tqdm(desc='Progress     ', total=(1 << 24), ascii=(common.PY_IMPLEMENTATION == 'PyPy'))
    constructible_bar: tqdm = tqdm(desc='Constructible', total=(1 << 24), ascii=(common.PY_IMPLEMENTATION == 'PyPy'))

    constructible_count: int = 0
    for r in range(256):
        for g in range(256):
            for b in range(256):
                solver_result: list[SearchNode] | None = solve((r, g, b))
                progress_bar.update(1)
                if solver_result is not None:
                    constructible_bar.update(1)
                    constructible_count += 1

    print(f'{constructible_count} / {1 << 24} ({constructible_count / (1 << 24):.3%}) colors constructible.')
    print(f'{(1 << 24) - constructible_count} / {1 << 24} ({1 - (constructible_count / (1 << 24)):.3%}) colors unconstructible.')
