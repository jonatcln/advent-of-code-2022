from abc import ABC, abstractmethod
from dataclasses import dataclass, astuple
from typing import Iterator, Literal, TypeVar
import itertools


__all__ = [
    'Point', 'FrozenPoint', 'MutablePoint', 'astuple',
    'norm', 'supnorm', 'distance', 'supdistance', 'normalized',
    'adjacents', 'diagonally_adjacents', 'all_adjacents',
]


PointT = TypeVar('PointT', bound='Point')


class Point(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def x(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def y(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def __init__(self, x: int, y: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __eq__(self, rhs: 'Point') -> bool:
        return self.x == rhs.x and self.y == rhs.y

    def __iter__(self) -> Iterator[int]:
        return iter((self.x, self.y))

    def __len__(self) -> Literal[2]:
        return 2

    def __getitem__(self, component: int | str) -> int:
        if isinstance(component, int):
            return (self.x, self.y)[component]
        elif isinstance(component, str):
            if component == 'x':
                return self.x
            elif component == 'y':
                return self.y
            else:
                raise IndexError
        else:
            raise TypeError

    def __neg__(self: PointT) -> PointT:
        return type(self)(-self.x, -self.y)

    def __add__(self: PointT, rhs: 'Point') -> PointT:
        return type(self)(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self: PointT, rhs: 'Point') -> PointT:
        return type(self)(self.x - rhs.x, self.y - rhs.y)

    def __mul__(self: PointT, rhs: int) -> PointT:
        return type(self)(self.x * rhs, self.y * rhs)

    def __rmul__(self: PointT, lhs: int) -> PointT:
        return type(self)(lhs * self.x, lhs * self.y)

    def __floordiv__(self: PointT, value: int) -> PointT:
        return type(self)(self.x // value, self.y // value)

    def __truediv__(self, _):
        return NotImplemented


@dataclass(frozen=True, slots=True)
class FrozenPoint(Point):
    x: int
    y: int

    def __repr__(self) -> str:
        return f'FrozenPoint({self.x}, {self.y})'

    def to_mutable(self) -> 'MutablePoint':
        return MutablePoint(self.x, self.y)


class MutablePoint(Point):
    __slots__ = 'x', 'y'

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'MutablePoint({self.x}, {self.y})'

    def __iadd__(self, rhs: Point) -> 'MutablePoint':
        self.x += rhs.x
        self.y += rhs.y
        return self

    def __isub__(self, rhs: Point) -> 'MutablePoint':
        self.x -= rhs.x
        self.y -= rhs.y
        return self

    def __imul__(self, rhs: int) -> 'MutablePoint':
        self.x *= rhs
        self.y *= rhs
        return self

    def __ifloordiv__(self, rhs: int) -> 'MutablePoint':
        self.x //= rhs
        self.y //= rhs
        return self

    def normalize(self) -> None:
        self.x = int(self.x > 0) - int(self.x < 0)
        self.y = int(self.y > 0) - int(self.y < 0)

    def flip(self) -> None:
        self.x = -self.x
        self.y = -self.y

    def flip_x(self) -> None:
        self.x = -self.x

    def flip_y(self) -> None:
        self.y = -self.y

    def to_frozen(self) -> FrozenPoint:
        return FrozenPoint(self.x, self.y)


def norm(p: Point) -> int:
    """Return the L1-norm (= L1-distance to origin = "Manhatten length")."""
    return abs(p.x) + abs(p.y)


def supnorm(p: Point) -> int:
    """Return the sup norm."""
    return max(abs(p.x), abs(p.y))


def normalized(p: PointT) -> PointT:
    return type(p)(
        int(p.x > 0) - int(p.x < 0),
        int(p.y > 0) - int(p.y < 0)
    )


def distance(p: Point, q: Point) -> int:
    """Return the L1-distance (= "Manhatten distance") to another point."""
    return norm(p - q)


def supdistance(p: Point, q: Point) -> int:
    """Return the Chebyshev distance to another point."""
    return supnorm(p - q)


def adjacents(p: PointT) -> Iterator[PointT]:
    yield type(p)(p.x, p.y - 1)
    yield type(p)(p.x - 1, p.y)
    yield type(p)(p.x + 1, p.y)
    yield type(p)(p.x, p.y + 1)


def diagonally_adjacents(p: PointT) -> Iterator[PointT]:
    for dx, dy in itertools.product((-1, 1), repeat=2):
        yield type(p)(p.x + dx, p.y + dy)


def all_adjacents(p: PointT) -> Iterator[PointT]:
    for dx, dy in itertools.product((-1, 0, 1), repeat=2):
        if dx != 0 or dy != 0:
            yield p + FrozenPoint(dx, dy)
