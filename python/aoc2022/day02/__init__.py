from aoc2022.manager import aoc


Value = int


@aoc.solver(day=2, part=1)
def part1(data: str):
    strategy_guide = parse(data)

    def total_score(opp_shape: Value, my_shape: Value) -> int:
        outcome = (my_shape - opp_shape + 1) % 3
        return score(my_shape) + 3 * outcome

    return sum(total_score(*rnd) for rnd in strategy_guide)


@aoc.solver(day=2, part=2)
def part2(data: str):
    strategy_guide = parse(data)

    def total_score(opp_shape: Value, target_outcome: Value):
        my_shape = (opp_shape + (target_outcome - 1)) % 3
        return score(my_shape) + 3 * target_outcome

    return sum(total_score(*rnd) for rnd in strategy_guide)


def parse(data: str) -> list[tuple[Value, Value]]:
    return [tuple(map(to_value, line.split())) for line in data.splitlines()]


def to_value(s: str) -> Value:
    return ord(s) - (ord('A') if ord(s) < ord('X') else ord('X'))


def score(v: Value) -> int:
    return v + 1
