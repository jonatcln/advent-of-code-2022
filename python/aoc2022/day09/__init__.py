from itertools import pairwise
from typing import NamedTuple

from aoc2022.manager import aoc
from aoc2022.utils import Point, MutablePoint, normalized, parse_direction, supdistance


@aoc.solver(day=9)
def run(data: str):
    motions = list(map(parse_motion, data.splitlines()))
    return simulate(create_rope(2), motions), simulate(create_rope(10), motions)


def parse_motion(raw: str) -> tuple[Point, int]:
    rd, rs = raw.split()
    return parse_direction(rd), int(rs)


def create_rope(knots: int) -> list[MutablePoint]:
    return [MutablePoint(0, 0) for _ in range(knots)]


def simulate(rope: list[MutablePoint], motions: list[tuple[Point, int]]) -> int:
    positions = {rope[-1].to_frozen()}
    for direction in (d for d, steps in motions for _ in range(steps)):
        rope[0] += direction
        for leader, follower in pairwise(rope):
            if supdistance(leader, follower) <= 1:
                break
            follower += normalized(leader - follower)
        positions.add(rope[-1].to_frozen())
    return len(positions)
