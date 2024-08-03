from typing import List, Set
from unittest import main

from base_test import BaseTest
from maze import Maze


class EmptyMaze(Maze):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()


class TestMaze(BaseTest):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def test_meta_maze_injection(self):
        maze = EmptyMaze()
        d = maze.__dict__
        self.log(d)
        self.log(maze.description)
        for k in Maze.__metaclass__.required_attributes_for_maze:
            self.logged_assert(self, self.assertIn, (k, d))
            self.logged_assert(self, self.assertIsNone, (d[k],))


if __name__ == "__main__":
    main()
