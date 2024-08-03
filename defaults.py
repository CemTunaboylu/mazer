from typing import List, Tuple
from itertools import product

from styles import bcolors, color_text, color_values_of
from dtypes import Vector
from maze import Maze, MazeValue


class DefaultMazeValue(MazeValue):
    WALL = "◼"
    # "●○◎◉⦿◇❖✪⊕⊖⊗⊘⊙⊚⊛⊜⊝⨀⨴⨵⨶⨳⨷⨸⩇⟐⟡⦾⦿⧀⧁⧂⧉⧈⧇⧆⧳⧲⧱⧰⧯⧮⧬⧭"
    PATH = "☐"
    FILLER = "‧"

    @staticmethod
    def get_playable() -> Tuple:
        return (DefaultMazeValue.PATH,)

    @staticmethod
    def get_unplayable() -> Tuple:
        return (DefaultMazeValue.WALL,)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class DefaultMaze(Maze):
    def __init__(self, space, maze_value_class=DefaultMazeValue) -> None:
        self.space = space
        self.dims = None
        self.dim()
        self.num_nodes = None
        self.num_nodes_in()
        self.playable = maze_value_class.get_playable()
        super().__init__()

    def __str__(self) -> str:
        return color_values(self, self.playable)

    def __repr__(self) -> str:
        return color_values(self, self.playable)


def __cum_product(dims: List[int]) -> List[int]:
    n = []
    cur = 1
    for d in reversed(dims):
        cur *= d
        n.append(cur)
    return list(reversed(n))


def color_path(maze: Maze, path: List[Vector], color: str = bcolors.OKBLUE) -> str:
    if not path:
        return ""
    path_set = set(path)
    to_print = [""]

    newline_breaks = set(__cum_product(maze.dims))

    for i, coor in enumerate(product(*(range(d) for d in maze.dims))):
        coor = Vector(coor)
        v = str(maze.get_value(coor))
        if coor in path_set:
            v = color_text(v, color, bold=True)

        to_print.append(v)
        for b in newline_breaks:
            if i % b == b - 1:
                to_print.append("\n")
    return "".join(to_print)


def color_values(
    maze: Maze,
    to_color: Tuple[str] = DefaultMazeValue.get_playable(),
    color: str = bcolors.OKGREEN,
):
    to_print = []
    newline_breaks = set(__cum_product(maze.dims[:-1]))

    c = 0
    for values in product(*(range(d) for d in maze.dims[:-1])):
        last_dim = maze.get_value(values)
        v = color_values_of(last_dim, to_color, color, bold=True)
        c += maze.dims[-1]
        to_print.append(v)
        for b in newline_breaks:
            if c % b == 0:
                to_print.append("\n")
    return "".join(to_print)
