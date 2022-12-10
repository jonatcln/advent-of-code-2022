import collections
import itertools
from typing import Callable, Iterable, Iterator, TypeVar

from .point import MutablePoint


__all__ = ['chunks', 'sliding_window', 'starfilter', 'parse_direction']


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


ItT = TypeVar('ItT', bound=Iterable)

def starfilter(
    function: Callable[..., bool],
    iterable: Iterable[ItT]
) -> Iterator[ItT]:
    return (x for x in iterable if function(*x))


def parse_direction(raw: str, flip_y=False) -> MutablePoint:
    p = MutablePoint(int(raw in {'R', 'E'}) - int(raw in {'L', 'W'}),
                     int(raw in {'U', 'N'}) - int(raw in {'D', 'S'}))
    if flip_y:
        p.flip_y()
    return p
