from typing import Iterable, Iterator, TypeVar
import collections
import itertools


T = TypeVar('T')


def chunks(seq: Iterable[T], size: int) -> Iterator[list[T]]:
    """Iterator over chunks of size `size` extracted sequentially from `seq`."""
    seq = iter(seq)
    while chunk := list(itertools.islice(seq, size)):
        yield chunk


def sliding_window(seq: Iterable[T], n: int) -> Iterator[tuple[T]]:
    """Return overlapping windows of size n."""
    # From the Itertools Recipes from the Python docs
    seq = iter(seq)
    window = collections.deque(itertools.islice(seq, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in seq:
        window.append(x)
        yield tuple(window)
