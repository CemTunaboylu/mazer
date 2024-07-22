from typing import List, Set
from unittest import main

from base_test import BaseTest
from defaults import DefaultMazeValue
from maze import Maze


def to_set(l: List[List]) -> Set:
    s = set()
    for elm in l:
        s.add(tuple(elm))
    return s


class TestDefaults(BaseTest):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def test_default_neighbor_shifts_for(self):
        # including_diagonal_movement = to_set(default_neighbor_shifts_for(2, True))
        # self.assertEqual(
        #     including_diagonal_movement,
        #     {
        #         (1, 0),
        #         (0, 1),
        #         (-1, 0),
        #         (0, -1),
        #         (1, 1),
        #         (-1, -1),
        #         (-1, 1),
        #         (1, -1),
        #     },
        # )
        only_orthogonal_movement = to_set(Maze.default_neighbor_shifts_for(2, False))
        self.assertEqual(
            only_orthogonal_movement,
            {
                (1, 0),
                (0, 1),
                (-1, 0),
                (0, -1),
            },
        )

        only_orthogonal_movement = to_set(Maze.default_neighbor_shifts_for(3, False))
        self.assertEqual(
            only_orthogonal_movement,
            {
                (1, 0, 0),
                (-1, 0, 0),
                (0, 1, 0),
                (0, -1, 0),
                (0, 0, 1),
                (0, 0, -1),
            },
        )

    def test_can_play_to(self):
        dmz = DefaultMazeValue
        test_cases = [
            # form, to, dir, exp
            # does not matter which dir
            (dmz.WALL, dmz.HORIZONTAL_PATH, [0, 1], False),
            (
                dmz.HORIZONTAL_PATH,
                dmz.WALL,
                [1, 0],
                False,
            ),
            (
                dmz.HORIZONTAL_PATH,
                dmz.VERTICAL_PATH,
                [1, 0],
                False,
            ),
            (
                dmz.VERTICAL_PATH,
                dmz.WALL,
                [0, 1],
                False,
            ),
            (
                dmz.VERTICAL_PATH,
                dmz.HORIZONTAL_PATH,
                [0, 1],
                True,
            ),
            (
                dmz.HORIZONTAL_PATH,
                dmz.VERTICAL_PATH,
                [0, 1],
                True,
            ),
            (
                dmz.VERTICAL_PATH,
                dmz.VERTICAL_PATH,
                [0, 1],
                True,
            ),
            (
                dmz.HORIZONTAL_PATH,
                dmz.HORIZONTAL_PATH,
                [0, 1],
                True,
            ),
            (
                dmz.HORIZONTAL_PATH,
                dmz.HORIZONTAL_PATH,
                [1, 0],
                False,
            ),
        ]

        for frm, to, dir, exp in test_cases:
            r = frm.can_play_to(to, dir)
            self.assertEqual(exp, r)


if __name__ == "__main__":
    main()
