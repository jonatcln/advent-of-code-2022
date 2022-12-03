from typing import Iterable, Iterator, TypeVar
import itertools


T = TypeVar('T')


def chunks(seq: Iterable[T], size: int) -> Iterator[list[T]]:
    """Iterator over chunks of size `size` extracted sequentially from `seq`."""
    seq = iter(seq)
    while chunk := list(itertools.islice(seq, size)):
        yield chunk
