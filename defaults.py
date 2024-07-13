from enum import Enum
from typing import Generator, List

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

    def __repr__(self):
        return str(self.value)


# TODO: color the path
def show_path(maze: Maze, path: List[Position]):
    [print(m) for m in maze.space]
