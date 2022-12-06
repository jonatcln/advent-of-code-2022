from typing import Iterable

from aoc2022.manager import aoc
from aoc2022.utils import sliding_window


@aoc.solver(day=6)
def run(data: str):
    stream = data.splitlines()[0]
    return first_marker_index(stream, 4), first_marker_index(stream, 14)


def first_marker_index(stream: Iterable[str], n: int) -> int:
    """Find the index right after the first marker of size `n` in `stream`."""
    stream = iter(stream)
    for i, marker in enumerate(sliding_window(stream, n)):
        if len(set(marker)) == n:
            return i + n
    raise AssertionError("stream doens't contain markers of size n")
