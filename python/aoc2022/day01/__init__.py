from aoc2022.manager import aoc


@aoc.solver(day=1)
def run(data: str):
    bags = [[int(food) for food in bag.splitlines()]
            for bag in data.split('\n\n')]
    calories = [sum(x) for x in bags]
    return max(calories), sum(sorted(calories, reverse=True)[:3])
