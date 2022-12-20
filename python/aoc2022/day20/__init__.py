from dataclasses import dataclass, field
from itertools import pairwise
from typing import Iterable

from aoc2022.manager import aoc


@aoc.solver(day=20)
def run(data: str) -> tuple[int, int]:
    encrypted_file = [int(x) for x in data.splitlines()]
    return decrypt(encrypted_file), decrypt(encrypted_file, 811589153, 10)


def decrypt(
    encrypted_file: Iterable[int],
    encryption_key: int = 1,
    mix_rounds: int = 1
) -> int:
    """
    Decrypt the data and return the sum of the grove coordinates' components.
    """
    nodes = [Node(encryption_key * x) for x in encrypted_file]

    for n1, n2 in pairwise(nodes):
        n1.next = n2
        n2.prev = n1

    nodes[0].prev = nodes[-1]
    nodes[-1].next = nodes[0]

    for _ in range(mix_rounds):
        for node in nodes:
            if node.value > 0:
                target = node.forward(node.value % (len(nodes) - 1))
            elif node.value < 0:
                target = node.backward(abs(node.value - 1) % (len(nodes) - 1))
            else:
                continue

            node.prev.next = node.next
            node.next.prev = node.prev
            node.next = target.next
            node.prev = target
            target.next.prev = node
            target.next = node

    zero_node = next(n for n in nodes if n.value == 0)

    return sum((zero_node.forward(i % (len(nodes) - 1)).value
                for i in (1000, 2000, 3000)))


@dataclass(slots=True)
class Node:
    value: int
    prev: 'Node' = field(init=False)
    next: 'Node' = field(init=False)

    def forward(self, steps: int) -> 'Node':
        target = self
        for _ in range(steps):
            target = target.next
        return target

    def backward(self, steps: int) -> 'Node':
        target = self
        for _ in range(steps):
            target = target.prev
        return target
