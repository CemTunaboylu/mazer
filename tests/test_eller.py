from unittest import main

from base_test import BaseTest
from defaults import DefaultMaze, color_path
from dtypes import Vector
from eller import (
    convert_to_row,
    ellers_algorithm,
    reuse_disjoint_set,
    pretty_print,
    EllerMazeValue,
)
from styles import underline
from traversal import djikstra
from test_helpers import debug
from union_find import DisjointSet


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
        r = "".join([v.value for v in r])
        exp = "|  ___|  _|    _|"
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
        play = EllerMazeValue.get_playable()[0]
        for dims in test_cases:
            rows = ellers_algorithm(dims)
            self.log(pretty_print(rows))

            maze = DefaultMaze(rows, maze_value_class=EllerMazeValue)
            start_row = rows[1].index(EllerMazeValue.FULL_PATH)
            target_row = (
                len(rows[-1])
                - list(reversed(rows[-1])).index(EllerMazeValue.HORIZONTAL_PATH)
                - 1
            )

            target = (len(rows) - 1, target_row)
            path = djikstra(
                maze,
                Vector((0, start_row)),
                Vector(target),
            )
            replacements = {
                " ": EllerMazeValue.FILLER.value,
                "_": underline(EllerMazeValue.FILLER.value),
            }

            def replace(v: EllerMazeValue):
                v = v.value
                if v in replacements:
                    v = replacements[v]
                return v

            for i, r in enumerate(rows):
                rows[i] = [replace(dmv) for dmv in r]
            self.log(f"{EllerMazeValue.HORIZONTAL_PATH.value * len(maze.space[0])}")
            self.log(color_path(maze, path))
            self.logged_assert(self, self.assertIsNotNone, (path,))
            self.logged_assert(self, self.assertTrue, (len(path) > 0,))
            self.debug()


if __name__ == "__main__":
    main()
