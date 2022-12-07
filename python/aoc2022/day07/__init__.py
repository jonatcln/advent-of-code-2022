from abc import ABC, abstractmethod
from typing import Optional, Iterator

from aoc2022.manager import aoc


@aoc.solver(day=7)
def run(data: str) -> tuple[int, int]:
    terminal = Terminal()

    assert data[:2] == '$ '
    for command, *output in map(str.splitlines, data[2:].split('\n$ ')):
        terminal.reverse_execute(command, output)

    assert (cwd := terminal.cwd()) is not None
    root = cwd.get_root()

    return part1(root), part2(root)


def part1(root: 'Directory') -> int:
    sizes = (d.compute_size() for d in iter_all_directories(root))
    return sum(s for s in sizes if s <= 100000)


def part2(root: 'Directory') -> int:
    sizes = (d.compute_size() for d in iter_all_directories(root))
    used_space = root.compute_size()
    disk_space, required_unused_space = 70000000, 30000000
    max_allowed_space = disk_space - required_unused_space
    space_to_delete = used_space - max_allowed_space
    return min(s for s in sizes if s >= space_to_delete)


class FSNode(ABC):
    _name: str
    _parent: Optional['Directory']

    def __init__(self, name: str, parent: Optional['Directory'] = None) -> None:
        self._name = name
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> Optional['Directory']:
        return self._parent

    @parent.setter
    def parent(self, value: Optional['Directory']) -> None:
        assert value is not self
        self._parent = value

    @abstractmethod
    def compute_size(self) -> int:
        raise NotImplementedError


class Directory(FSNode):
    _children: dict[str, FSNode]

    def __init__(self, name: str, parent: Optional['Directory'] = None) -> None:
        super().__init__(name, parent)
        self._children = dict()

    @property
    def subdirectories(self) -> list['Directory']:
        return [d for d in self._children.values() if isinstance(d, Directory)]

    # override
    def compute_size(self) -> int:
        return sum(x.compute_size() for x in self._children.values())

    def has_child(self, name: str) -> bool:
        return name in self._children

    def get_child(self, name: str) -> Optional[FSNode]:
        return self._children[name]

    def add_child(self, node: FSNode) -> None:
        assert node is not self and node is not self.parent
        if isinstance(node, Directory):
            node.parent = self
        self._children[node.name] = node

    def get_root(self) -> 'Directory':
        if self.parent is None:
            return self
        return self.parent.get_root()


class File(FSNode):
    _size: int

    def __init__(
        self,
        name: str,
        size: int,
        parent: Optional['Directory'] = None
    ) -> None:
        super().__init__(name, parent)
        self._size = size

    # override
    def compute_size(self) -> int:
        return self._size


class Terminal:
    _cwd: Optional[Directory]

    def __init__(self) -> None:
        self._cwd = None

    def cwd(self) -> Optional[Directory]:
        return self._cwd

    def reverse_execute(self, command: str, output: list[str]) -> None:
        cmd_name, *cmd_args = command.split()
        if cmd_name == 'cd':
            assert len(cmd_args) == 1
            self.cd(cmd_args[0])
        elif cmd_name == 'ls':
            self.reverse_ls(output)
        else:
            raise AssertionError(f'unknown command: {cmd_name}')

    def cd(self, path: str) -> None:
        if path == '..':
            assert self._cwd and self._cwd.parent
            self._cwd = self._cwd.parent
        elif self._cwd is None:
            self._cwd = Directory(path)
        else:
            self._cwd = self.mkdir(path)

    def reverse_ls(self, output: list[str]) -> None:
        assert self._cwd is not None
        for specifier, name in map(str.split, output):
            if specifier == 'dir':
                self.mkdir(name)
            else:
                self.touch(name, size=int(specifier))

    def mkdir(self, name: str) -> Directory:
        assert self._cwd is not None
        if self._cwd.has_child(name):
            node = self._cwd.get_child(name)
            if not isinstance(node, Directory):
                raise AssertionError(
                    f'an incompatible node named `{name}` already exists')
            return node
        self._cwd.add_child(d := Directory(name))
        return d

    def touch(self, name: str, size: int) -> File:
        assert self._cwd is not None
        if self._cwd.has_child(name):
            node = self._cwd.get_child(name)
            if not isinstance(node, File) or not node.compute_size() == size:
                raise AssertionError(
                    f'an incompatible node named `{name}` already exists')
            return node
        self._cwd.add_child(f := File(name, size))
        return f


def iter_all_directories(root: Directory) -> Iterator[Directory]:
    yield root
    for d in root.subdirectories:
        yield from iter_all_directories(d)
