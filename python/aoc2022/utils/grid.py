from copy import copy
from typing import (Callable, Generic, Iterable, Iterator,
                    List, Optional, Type, TypeVar)

from . import chunks
from .point import Point, FrozenPoint


__all__ = ['Grid']


T = TypeVar('T')
Self = TypeVar('Self', bound='Grid')


class Grid(Generic[T]):
    _width: int
    _height: int
    grid: list[list[T]]

    def __init__(self) -> None:
        self._width = 0
        self._height = 0
        self.grid = [[]]

    @classmethod
    def new_empty(
        cls: Type[Self],
        width: int,
        height: int,
        init_value: T,
        make_copies: bool = False
    ) -> Self:
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
        cls: Type[Self],
        width: int,
        height: int,
        factory: Callable[[Point], T]
    ) -> Self:
        grid = cls()
        grid._width = width
        grid._height = height
        grid.grid = [[factory(FrozenPoint(x, y)) for x in range(width)]
                     for y in range(height)]
        return grid

    @classmethod
    def from_matrix(cls: Type[Self], matrix: List[List[T]]) -> Self:
        grid = cls()
        grid._height = len(matrix)
        grid._width = len(matrix[0])
        grid.grid = matrix
        return grid

    @classmethod
    def from_iter(cls: Type[Self], width: int, seq: Iterator[T]) -> Self:
        grid = cls.from_matrix(list(chunks(seq, width)))
        return grid

    @classmethod
    def parse(
        cls: Type[Self],
        raw: str,
        char_to_symbol: Callable[[str], T]
    ) -> Self:
        data = [[char_to_symbol(c) for c in line] for line in raw.splitlines()]
        return cls.from_matrix(data)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def __copy__(self) -> 'Grid':
        return type(self).from_matrix(self.grid)

    def copy(self) -> 'Grid':
        global copy
        return copy(self)

    def __str__(self) -> str:
        return '\n'.join(''.join(str(v) for v in row) for row in self.grid)

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
                yield FrozenPoint(x, y)

    def values(self) -> Iterable[T]:
        """Return an iterator over all values in Z-order."""
        return iter(self)

    def items(self) -> Iterator[tuple[Point, T]]:
        """
        Return an iterator over (point, value) pairs for all points in Z-order.
        """
        for y in range(self._height):
            for x, item in enumerate(self.grid[y]):
                yield FrozenPoint(x, y), item

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
