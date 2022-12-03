from aoc2022.manager import aoc
from aoc2022.utils import chunks
from typing import Iterable


@aoc.solver(day=3)
def run(data: str):
    rucksacks = data.splitlines()
    return (
        shared_items_priority_sum(compartments(r) for r in rucksacks),
        shared_items_priority_sum(chunks(rucksacks, 3))
    )


def compartments(rucksack: str) -> tuple[str, str]:
    """Extract the two equal compartments of the rucksack."""
    s = len(rucksack) // 2
    return rucksack[:s], rucksack[s:]


def shared_items_priority_sum(groups_list: Iterable[Iterable[str]]) -> int:
    """Calculate the sum of the priority of the shared item of each group."""
    return sum(priority(shared_items(*x)) for x in groups_list)


def shared_items(*groups: str) -> str:
    """Find the single item shared by all groups."""
    shared = set(groups[0]).intersection(*groups[1:])
    assert (len(shared) == 1)
    return next(iter(shared))


def priority(item: str) -> int:
    """Get the priority of the given item type."""
    c = ord(item)
    return (c - ord('A') + 27) if c < ord('a') else (c - ord('a') + 1)
