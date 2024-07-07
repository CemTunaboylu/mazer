from typing import List, Set
from unittest import TestCase, main

from defaults import default_neighbor_shifts_for


def to_set(l: List[List]) -> Set:
    s = set()
    for elm in l:
        s.add(tuple(elm))
    return s


class TestDefaults(TestCase):
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
        only_orthogonal_movement = to_set(default_neighbor_shifts_for(2, False))
        self.assertEqual(
            only_orthogonal_movement,
            {
                (1, 0),
                (0, 1),
                (-1, 0),
                (0, -1),
            },
        )

        only_orthogonal_movement = to_set(default_neighbor_shifts_for(3, False))
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


if __name__ == "__main__":
    main()
