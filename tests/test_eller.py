from unittest import main

from base_test import BaseTest
from defaults import color_path, DefaultMazeValue, show_bits
from dtypes import Vector, sub
from generators.eller import (
    convert_to_row,
    ellers_algorithm,
    reuse_disjoint_set,
)
from styles import underline
from traversal import djikstra
from test_helpers import debug
from generators.union_find import DisjointSet


class TestEller(BaseTest):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.debug_mode = False

    def test_convert_to_row(self):
        p = [0, 0, 0, 3, 3, 5, 5, 5]
        r = [3, 1, 1, 2, 1, 3, 1, 1]
        v = {0, 3, 5, 6}
        L = len(p)
        d = DisjointSet(L, parents=p, ranks=r)
        r = convert_to_row(d, v)
        r = "-".join([show_bits(v.value) for v in r])
        exp = "0101-0011-0010-0101-0010-0101-0111-0010"
        self.assertEqual(exp, r, f"{exp}!={r}")

    def test_reuse_disjoint_set(self):
        p = [0, 0, 0, 3, 3, 5, 5, 5]
        r = [3, 1, 1, 2, 1, 3, 1, 1]
        v = {0, 3, 5, 6}
        L = len(p)
        d = DisjointSet(L, parents=p, ranks=r)
        reuse_disjoint_set(d, v)
        self.assertListEqual([0, 1, 2, 3, 4, 5, 5, 7], d.parents)
        self.assertListEqual([1, 1, 1, 1, 1, 2, 1, 1], d.ranks)

    def test_eller_is_fully_connected(self):
        test_cases = [(3, 7), (15, 15), (28, 28)]
        for dims in test_cases:
            maze = ellers_algorithm(dims)

            path = djikstra(
                maze,
                Vector((0, 0)),
                Vector(sub(dims, (1, 1))),
            )
            self.logged_assert(self, self.assertIsNotNone, (path,))
            self.log(f"{'_'* len(maze.space[0])}")
            self.log(color_path(maze, path))
            self.debug()


if __name__ == "__main__":
    main()
