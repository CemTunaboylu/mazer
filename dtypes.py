from typing import List, NewType, Tuple, Union
from abc import ABC, abstractmethod

Position = NewType("Position", Tuple[int, ...])
Number = Union[float, int]


class MazeValue(ABC):

    @abstractmethod
    def is_playable(self) -> bool:
        pass

    @staticmethod
    def get_playable():
        pass


Maze = NewType("Maze", List[List | MazeValue])
