from typing import Callable, Iterator

from aoc2022.manager import aoc


@aoc.solver(day=4)
def run(data: str):
    section_assignments = list(parse(data))
    return (
        overlap_count(section_assignments, overlap_fully),
        overlap_count(section_assignments, overlap_partially)
    )


def parse(data: str) -> Iterator[tuple[int, int, int, int]]:
    for line in data.splitlines():
        yield tuple(int(x) for p in line.split(',') for x in p.split('-'))


def overlap_count(
    section_assignments: list[tuple[int, int, int, int]],
    check_overlap: Callable[[int, int, int, int], bool],
):
    """
    Count the number of assignment pairs that overlap according to a predicate.
    """
    return sum(int(check_overlap(*bounds)) for bounds in section_assignments)


def overlap_fully(start1, end1, start2, end2) -> bool:
    """Check if the ranges [start1, end1] and [start2, end2] fully overlap."""
    return (start2 - start1) * (end2 - end1) <= 0


def overlap_partially(start1, end1, start2, end2) -> bool:
    """Check if the ranges [start1, end1] and [start2, end2] overlap at all."""
    return (end2 - start1) * (start2 - end1) <= 0
