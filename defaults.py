from enum import Enum
from typing import List
from itertools import product

from colors import color_text, bcolors
from dtypes import Position
from maze import Maze


class DefaultMazeValue(Enum):
    WALL = 0
    PATH = 1

    def is_playable(self) -> bool:
        return self == DefaultMazeValue.PATH

    @staticmethod
    def get_playable():
        return DefaultMazeValue.PATH

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class DefaultMaze(Maze):
    def __init__(self, space) -> None:
        self.space = space
        self.dims = self.dim()
        self.playable = self.get_value(
            Position([0] * len(self.dims))
        ).__class__.get_playable()

        super().__init__()


def __cum_product(dims: List[int]) -> List[int]:
    n = []
    cur = 1
    for d in reversed(dims):
        cur *= d
        n.append(cur)
    return list(reversed(n))


def color_path(maze: Maze, path: List[Position], color: str):
    space = maze.space
    stack = [space]
    path_set = set(path)
    to_print = [""]

    newline_breaks = set(__cum_product(maze.dims))

    for i, coor in enumerate(product(*(range(d) for d in maze.dims))):
        coor = Position(coor)
        v = str(maze.get_value(coor))
        if coor in path_set:
            v = color_text(v, color, bold=True)

        to_print.append(v)
        for b in newline_breaks:
            if i % b == b - 1:
                to_print.append("\n")
    return " ".join(to_print)
