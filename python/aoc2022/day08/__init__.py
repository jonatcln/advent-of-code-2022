from functools import partial
from math import prod
from typing import Iterator

from aoc2022.manager import aoc
from aoc2022.utils import Grid, Point


@aoc.solver(day=8)
def run(data: str) -> tuple[int, int]:
    grid = Grid.parse(data, int)
    return part1(grid), part2(grid)


def part1(grid: Grid[int]) -> int:
    return sum(1 for p in grid.points() if is_visible(p, grid))


def part2(grid: Grid[int]) -> int:
    return max(scenic_score(p, grid) for p in grid.points())


def is_visible(point: Point, grid: Grid[int]) -> bool:
    tree = grid[point]
    return any(max(v) < tree if v else True for v in get_views(point, grid))


def scenic_score(point: Point, grid: Grid[int]) -> int:
    tree = grid[point]
    return prod(map(partial(viewing_distance, tree), get_views(point, grid)))


def viewing_distance(tree: int, view: list[int]) -> int:
    return next((i+1 for i, h in enumerate(view) if h >= tree), len(view))


def get_views(point: Point, grid: Grid[int]) -> Iterator[list[int]]:
    row = list(grid.row(point.y))
    col = list(grid.col(point.x))
    yield row[:point.x][::-1]   # towards left edge
    yield row[point.x+1:]       # towards right edge
    yield col[:point.y][::-1]   # towards top edge
    yield col[point.y+1:]       # towards bottom edge
