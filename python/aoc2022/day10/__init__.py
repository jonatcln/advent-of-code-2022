from aoc2022.manager import aoc
from aoc2022.utils import chunks, starfilter

import re
from itertools import count, starmap
from typing import Iterator, Optional, TypedDict


@aoc.solver(day=10, part=1)
def part1(data: str) -> int:
    interesting_states = starfilter(is_interesting, run_instructions(data))
    return sum(starmap(signal_strength, interesting_states))


@aoc.solver(day=10, part=2)
def part2(data: str) -> str:
    screen = starmap(derive_pixel, run_instructions(data))
    return '\n'.join(''.join(x) for x in chunks(screen, 40))


class Registers(TypedDict):
    x: int
    p: int


def run_instructions(data: str) -> Iterator[tuple[int, int]]:
    """
    Run instructions and yield the cpu state at the start of each cycle.

    Yields (cycle, register['x']) pairs.
    """
    registers = Registers(x=1, p=1)
    for cycle, op in zip(count(start=1), to_cpu_operations(data)):
        yield cycle, registers['x']
        if op:
            registers[op[0]] += op[1]


def to_cpu_operations(raw: str) -> Iterator[Optional[tuple[str, int]]]:
    """
    Transform raw instructions in per-cycle cpu operations.

    Yields either `None` if it's a noop, or `(register, value)` pairs to denote
    that `value` should be added to `register`.
    """
    for instruction in raw.splitlines():
        yield None
        if instruction != 'noop':
            assert (m := re.fullmatch(r'add(\w) (-?\d+)', instruction))
            yield m.group(1), int(m.group(2))


def is_interesting(cycle: int, _x: int) -> bool:
    return cycle in {20, 60, 100, 140, 180, 220}

def signal_strength(cycle: int, x: int) -> int:
    return cycle * x

def derive_pixel(cycle: int, x: int) -> str:
        return '█' if (cycle - 1) % 40 in range(x-1, x+2) else ' '
