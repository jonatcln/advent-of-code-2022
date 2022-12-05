from itertools import takewhile
from typing import Iterator, NamedTuple
import re

from aoc2022.manager import aoc


@aoc.solver(day=5, part=1)
def part1(data: str):
    stacks, instructions = parse(data)
    for (n, from_i, to_i) in instructions:
        for _ in range(n):
            stacks[to_i].append(stacks[from_i].pop())
    return top_of_stacks_str(stacks)


@aoc.solver(day=5, part=2)
def part2(data: str):
    stacks, instructions = parse(data)
    for (n, from_i, to_i) in instructions:
        tail = stacks[from_i][-n:]
        del stacks[from_i][-n:]
        stacks[to_i].extend(tail)
    return top_of_stacks_str(stacks)


class Instruction(NamedTuple):
    """
    Instruction to move `amount` items from stack `from_i` to stack `to_i`.
    """
    amount: int  # number of items to move
    from_i: int  # 0-based stack index
    to_i: int    # 0-based stack index


def parse(data: str):
    raw_stacks, raw_instructions = data.split('\n\n')
    return parse_stacks(raw_stacks), parse_instructions(raw_instructions)


def parse_stacks(raw: str) -> list[list[str]]:
    cols = (line[1::4] for line in reversed(raw.splitlines()[:-1]))
    return [list(takewhile(str.isalpha, stack)) for stack in zip(*cols)]


def parse_instructions(raw: str) -> Iterator[Instruction]:
    for line in raw.splitlines():
        m = re.fullmatch(r'move (\d+) from (\d) to (\d)', line)
        assert m is not None
        values = list(map(int, m.groups()))
        yield Instruction(values[0], values[1] - 1, values[2] - 1)


def top_of_stacks_str(stacks: list[list[str]]) -> str:
    return ''.join(s[-1] for s in stacks)
