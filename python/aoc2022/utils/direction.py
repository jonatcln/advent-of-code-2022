import enum


__all__ = ['Direction']


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
