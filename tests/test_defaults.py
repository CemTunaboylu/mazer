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
        dmv = DefaultMazeValue
        play, unplay = (dmv.get_playable()[0], dmv.get_unplayable()[0])
        test_cases = [
            # form, to, dir, exp
            # does not matter which dir
            (unplay, play, [0, 1], False),
            (
                play,
                unplay,
                [1, 0],
                False,
            ),
            (
                play,
                play,
                [1, 0],
                True,
            ),
            (
                play,
                unplay,
                [0, 1],
                False,
            ),
            (
                play,
                play,
                [0, 1],
                True,
            ),
            (
                play,
                play,
                [0, 1],
                True,
            ),
            (
                play,
                play,
                [0, 1],
                True,
            ),
            (
                play,
                play,
                [0, 1],
                True,
            ),
        ]

        for frm, to, dir, exp in test_cases:
            self.log(f"{frm}, {to}, {dir}, {exp}")
            r = frm.can_play_to(to, dir)
            self.log(f"{r}")
            # self.assertEqual(exp, r)
            self.logged_assert(self, self.assertEqual, (exp, r))

    def test_custom_rules_for_can_play_to(self):
        dmv = DefaultMazeValue
        play = dmv.get_playable()[0]
        normally_playable = (
            play,
            play,
            [1, 0],
        )
        for rule_return in [True, False]:
            frm, to, dir = normally_playable
            r = frm.can_play_to(
                to, dir, lambda a, b: rule_return, lambda a, b: rule_return
            )
            self.assertEqual(rule_return, r)


if __name__ == "__main__":
    main()
