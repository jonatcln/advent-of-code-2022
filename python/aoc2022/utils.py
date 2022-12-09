from copy import copy
from functools import singledispatchmethod
from typing import Callable, Generic, Iterable, Iterator, List, Optional, TypeVar, overload
import collections
import enum
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


class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __iadd__(self, other: 'Point') -> 'Point':
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other: 'Point') -> 'Point':
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, value: int) -> 'Point':
        self.x *= value
        self.y *= value
        return self

    def __ifloordiv__(self, value: int) -> 'Point':
        self.x //= value
        self.y //= value
        return self

    def __neg__(self) -> 'Point':
        return Point(-self.x, -self.y)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    @singledispatchmethod
    def __mul__(self, _):
        raise NotImplementedError

    @__mul__.register(int)
    def _(self, value: int) -> 'Point':
        return Point(self.x * value, self.y * value)

    @__mul__.register(float)
    def _(self, value: float) -> 'GeometricPoint':
        return GeometricPoint(self.x * value, self.y * value)

    def __floordiv__(self, value: int) -> 'Point':
        return Point(self.x // value, self.y // value)

    def __truediv__(self, value: int | float) -> 'GeometricPoint':
        return GeometricPoint(self.x / value, self.y / value)

    def distance_to(self, p: 'Point') -> int:
        return abs(p.x - self.x) + abs(p.y - self.y)

    def distance_to_origin(self) -> int:
        return self.distance_to(Point(0, 0))

    def diagonally_adjacents(self) -> Iterator['Point']:
        for dx, dy in itertools.product((-1, 1), repeat=2):
            yield Point(self.x + dx, self.y + dy)

    def adjacents(self) -> Iterator['Point']:
        yield Point(self.x, self.y - 1)
        yield Point(self.x - 1, self.y)
        yield Point(self.x + 1, self.y)
        yield Point(self.x, self.y + 1)

    def adjacents_with_diagonals(self) -> Iterator['Point']:
        for dx, dy in itertools.product((-1, 0, 1), repeat=2):
            if dx != 0 or dy != 0:
                yield Point(self.x + dx, self.y + dy)

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'


class GeometricPoint:
    x: float
    y: float

    @overload
    def __init__(self, xp: int | float, y: int | float) -> None:
        ...

    @overload
    def __init__(self, xp: Point) -> None:
        ...

    def __init__(
        self,
        xp: int | float | Point,
        y: Optional[int | float] = None
    ) -> None:
        if isinstance(xp, Point):
            self.x, self.y = float(xp.x), float(xp.y)
        elif y is not None:
            self.x, self.y = float(xp), float(y)
        else:
            raise TypeError

    def distance_to(self, p: 'GeometricPoint') -> float:
        return ((p.x - self.x)**2 + (p.y - self.y)**2) ** 0.5

    def distance_to_origin(self) -> float:
        return self.distance_to(GeometricPoint(0.0, 0.0))

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'GeometricPoint({self.x}, {self.y})'


class Grid(Generic[T]):
    _width: int
    _height: int
    grid: list[list[T]]

    def __init__(self):
        self._width = 0
        self._height = 0
        self.grid = [[]]

    @classmethod
    def new_empty(
        cls,
        width: int,
        height: int,
        init_value: T,
        make_copies: bool = False
    ) -> 'Grid':
        grid = cls()
        grid._width = width
        grid._height = height
        if make_copies:
            grid.grid = [[copy(init_value) for _ in range(width)]
                         for _ in range(height)]
        else:
            grid.grid = [[init_value] * width for _ in range(height)]
        return grid

    @classmethod
    def new_empty_with_init(
        cls,
        width: int,
        height: int,
        factory: Callable[[Point], T]
    ) -> 'Grid':
        grid = cls()
        grid._width = width
        grid._height = height
        grid.grid = [[factory(Point(x, y)) for x in range(width)]
                     for y in range(height)]
        return grid

    @classmethod
    def from_matrix(cls, matrix: List[List[T]]) -> 'Grid':
        grid = cls()
        grid._height = len(matrix)
        grid._width = len(matrix[0])
        grid.grid = matrix
        return grid

    @classmethod
    def from_iter(cls, width: int, seq: Iterator[T]) -> 'Grid':
        grid = cls.from_matrix(list(chunks(seq, width)))
        return grid

    @classmethod
    def parse(cls, raw: str, char_to_symbol: Callable[[str], T]) -> 'Grid':
        data = [[char_to_symbol(c) for c in line] for line in raw.splitlines()]
        return cls.from_matrix(data)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def __copy__(self) -> 'Grid':
        cls = self.__class__
        grid = cls.__new__(cls)
        grid.__dict__.update(self.__dict__)
        for y in range(self._height):
            grid.grid[y] = grid.grid[y][:]
        return grid

    def __getitem__(self, key: Point) -> T:
        if isinstance(key, Point):
            if not self.has_pos(key):
                raise IndexError(f'point {key} is outside grid')
            return self.grid[key.y][key.x]
        else:
            raise TypeError

    def __setitem__(self, key: Point, value: T) -> None:
        if isinstance(key, Point):
            if not self.has_pos(key):
                raise IndexError(f'point {key} is outside grid')
            self.grid[key.y][key.x] = value
        else:
            raise TypeError

    def __contains__(self, item: T) -> bool:
        return any(item in row for row in self.grid)

    def __iter__(self) -> Iterator[T]:
        """Equivalent to `.values()`."""
        for row in self.grid:
            yield from row

    def points(self) -> Iterator[Point]:
        """Return an iterator over all points in Z-order."""
        for y in range(self._height):
            for x in range(self._width):
                yield Point(x, y)

    def values(self) -> Iterable[T]:
        """Return an iterator over all values in Z-order."""
        return iter(self)

    def items(self) -> Iterator[tuple[Point, T]]:
        """
        Return an iterator over (point, value) pairs for all points in Z-order.
        """
        for y in range(self._height):
            for x, item in enumerate(self.grid[y]):
                yield Point(x, y), item

    def rows(self) -> Iterator[list[T]]:
        """Return an iterator over copies of all rows."""
        yield from (row[:] for row in self.grid)

    def cols(self) -> Iterator[list[T]]:
        """Return an iterator over copies of all columns."""
        for x in range(self._width):
            yield [self.grid[y][x] for y in range(self._height)]

    def row(self, y: int) -> Iterator[T]:
        """Return an iterator over all elements of the row with index `y`."""
        return iter(self.grid[y])

    def col(self, x: int) -> Iterator[T]:
        """Return an iterator over all elements of the column with index `x`."""
        return (self.grid[y][x] for y in range(self._height))

    def has_pos(self, p: Point) -> bool:
        """Return if the point `p` is in this within the grid boundaries."""
        return 0 <= p.x < self._width and 0 <= p.y < self._height

    def get(self, p: Point) -> Optional[T]:
        if not self.has_pos(p):
            return None
        return self.grid[p.y][p.x]

    def reset(self, reset_value: T) -> None:
        """Reset all values to `reset_value`."""
        for p in self.points():
            self.grid[p.y][p.x] = reset_value

    def any(self, pred: Callable[[Point, T], bool]) -> bool:
        """
        Return if there's an item that for which the precicate returns True.
        """
        return any(pred(p, v) for p, v in self.items())

    def filter(
        self,
        pred: Callable[[Point, T], bool]
    ) -> Iterator[tuple[Point, T]]:
        """
        Return an iterator over all points for which the predicate returns True.
        """
        return ((p, v) for p, v in self.items() if pred(p, v))

    def map(self, f: Callable[[Point, T], T]) -> None:
        """
        Apply `f` to each element. `f` is a function `Point, old_val -> new_val`
        """
        for p, v in self.items():
            self.grid[p.y][p.x] = f(p, v)

    def find_value(self, value: T) -> Iterator[Point]:
        """
        Return an iterator over all points with a corresponding value of `value`.
        """
        return (p for p, v in self.items() if value == v)

    def replace(
        self,
        old_value: T,
        new_value: T,
        make_copies: bool = True
    ) -> None:
        """Replace every value equal to `old_value` by `new_value`."""
        if make_copies:
            for p in self.find_value(old_value):
                self.grid[p.y][p.x] = copy(new_value)
        else:
            for p in self.find_value(old_value):
                self.grid[p.y][p.x] = new_value

    def replace_with_init(
        self,
        old_value: T,
        factory: Callable[[Point], T]
    ) -> None:
        """
        Replace every value equal to `old_value` by a value created by `factory`.
        """
        for p in self.find_value(old_value):
            self.grid[p.y][p.x] = factory(p)

    def find_replace(
        self,
        pred: Callable[[Point, T], bool],
        new_value: T, make_copies: bool = True
    ) -> None:
        """
        Replace every value for which the predicate returns True by `new_value`.
        """
        if make_copies:
            for p, _ in self.filter(pred):
                self.grid[p.y][p.x] = copy(new_value)
        else:
            for p, _ in self.filter(pred):
                self.grid[p.y][p.x] = new_value

    def find_replace_with_init(
        self,
        pred: Callable[[Point, T], bool],
        factory: Callable[[Point, T], T]
    ) -> None:
        """
        Replace every value for which the predicate returns True by a value create by `factory`.
        """
        for p, v in self.filter(pred):
            self.grid[p.y][p.x] = factory(p, v)


class Direction(enum.Enum):
    U = N = UP = NORTH = 0
    R = E = RIGHT = EAST = 1
    D = S = DOWN = SOUTH = 2
    L = W = LEFT = WEST = 3

    def opposite(self) -> 'Direction':
        return self.rotate(2)

    def rotate_cw(self) -> 'Direction':
        return self.rotate(1)

    def rotate_ccw(self) -> 'Direction':
        return self.rotate(-1)

    def rotate(self, n: int) -> 'Direction':
        """Rotate n times 90 degrees. (to left if n < 0, to right if n > 0)"""
        return Direction((self.value + n) % 4)

    # Aliases

    def rotate_right(self) -> 'Direction':
        return self.rotate_cw()

    def rotate_left(self) -> 'Direction':
        return self.rotate_ccw()

    def mirror(self) -> 'Direction':
        return self.opposite()
