from enum import Enum
from typing import Generator, List

from dtypes import Maze, Position


class DefaultMazeValue(Enum):
    WALL = 0
    PATH = 1

    def is_playable(self) -> bool:
        return self == DefaultMazeValue.PATH

    @staticmethod
    def get_playable():
        return DefaultMazeValue.PATH

    def __repr__(self):
        return str(self.value)


def default_neighbor_shifts_for(
    dim: int,
    can_move_diagonally: bool = False,
    dirs: List[int] = [-1, 1],  # possible directions for each dimension
) -> Generator[Position, None, None]:

    # TODO: implement this
    if can_move_diagonally:
        pass

    # orthogonal movement only
    for d in range(dim):
        for i in dirs:
            n = [0] * dim
            n[d] = i
            yield Position(n)


def add(pos: Position, other: Position) -> Position:  # Generator[int, None, None]:
    # TODO: hold each position as a generator if dimensions are big?
    return tuple(p + o for p, o in zip(pos, other))


def is_same(pos: Position, other: Position) -> bool:
    return all(p == o for p, o in zip(pos, other))


def get_value(maze: Maze, coor: Position) -> DefaultMazeValue:
    v = None
    for c in coor:
        maze = maze[c]
    return maze


def set_value(maze: Maze, coor: Position, to):
    v = None
    for c in coor[:-1]:
        maze = maze[c]
    maze[coor[-1]] = to


# TODO: color the path
def show_path(maze: Maze, path: List[Position]):
    [print(m) for m in maze]
