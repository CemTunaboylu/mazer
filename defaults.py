from itertools import product
from typing import Any, Callable, List, Tuple, Union

from aenum import extend_enum

from styles import bcolors, color_text, color_values_of
from dtypes import Vector, Direction, directions
from maze import Maze, MazeValue


def show_bits(v):
    if not isinstance(v, int):
        v = v.value
    return bin(v)[2:].zfill(4)


def get_after_point(enm):
    e = str(enm)
    i = e.find(".")
    return e[i + 1 :]


def extend_dfs_maze_value_with(
    combined_enum=directions, stringer=get_after_point, join_with="-"
):
    try:
        for i in range(1, 2 ** len(combined_enum)):
            names = [stringer(d) for d in combined_enum if (d.value[-1] & i) > 0]
            name = join_with.join(names)
            extend_enum(DefaultMazeValue, f"{name}", i)
    except Exception as e:
        pass


class DefaultMazeValue(MazeValue):
    # <up_bit> <down_bit> <left_bit> <right_bit>
    NO_MOVE = 0

    @staticmethod
    def get_playable() -> Tuple:
        global playable
        return tuple(playable)

    @staticmethod
    def get_unplayable() -> Tuple:
        return (DefaultMazeValue.NO_MOVE,)

    def is_visited(self):
        return 0 != self.value

    # automatically makes the cell visited since the value is not 0 now
    def move(self, dir: Union[Direction, int]) -> "DefaultMazeValue":
        if isinstance(dir, Direction):
            dir = dir.get_bit()
        v = self.value | dir
        return DefaultMazeValue(v)

    def can_play_to(
        self,
        other: "DefaultMazeValue",
        dir: Direction,
        *rules_to_pass: Callable[["DefaultMazeValue", "DefaultMazeValue"], bool],
    ) -> bool:
        can_move_in = lambda x, y: (x.value & dir.get_bit()) and (
            y.value & dir.compliment()
        )

        rules = (can_move_in, *rules_to_pass)
        return super().can_play_to(other, dir, *rules)

    def __str__(self):
        return show_bits(self.value)

    def __repr__(self):
        return show_bits(self.value)


def merge(v1: DefaultMazeValue, v2: DefaultMazeValue) -> DefaultMazeValue:
    return DefaultMazeValue(v1.value | v2.value)


playable = list(DefaultMazeValue.__iter__())[1:]


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


# TOOD: move these out
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
    to_color: Tuple[Any, ...] = DefaultMazeValue.get_playable(),
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
