from unittest import main

from base_test import BaseTest
from defaults import DefaultMaze, DefaultMazeValue, color_path
from dtypes import Position
from eller import (
    convert_to_row,
    ellers_algorithm,
    reuse_disjoint_set,
    pretty_print,
    underline,
)
from traversal import djikstra
from test_helpers import ignore
from union_find import DisjointSet


class TestEller(BaseTest):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def test_convert_to_row(self):
        p = [0, 0, 0, 3, 3, 5, 5, 5]
        r = [3, 1, 1, 2, 1, 3, 1, 1]
        v = {0, 3, 5, 6}
        L = len(p)
        d = DisjointSet(L, parents=p, ranks=r)
        r = convert_to_row(d, v)
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
        test_cases = [(3, 7), (15, 15)]
        for dims in test_cases:
            rows = ellers_algorithm(dims)
            self.log(pretty_print(rows))
            row_values_to_maze_values(rows)

            maze = DefaultMaze(rows)
            start_row = rows[1].index(DefaultMazeValue.VERTICAL_PATH)
            target_row = (
                len(rows[-1])
                - list(reversed(rows[-1])).index(DefaultMazeValue.HORIZONTAL_PATH)
                - 1
            )

            target = (len(rows) - 1, target_row)
            path = djikstra(
                maze,
                Position((0, start_row)),
                Position(target),
            )
            if self.debug_mode:
                dmz = DefaultMazeValue
                replacements = {" ": dmz.FILLER.value, "_": underline(dmz.FILLER.value)}

                def replace(v: DefaultMazeValue):
                    v = v.value
                    if v in replacements:
                        v = replacements[v]
                    return v

                for i, r in enumerate(rows):
                    rows[i] = [replace(dmv) for dmv in r]
                    self.log(f"{'_' * len(maze.space[0])}")
                    self.log(color_path(maze, path))
            self.logged_assert(self, self.assertTrue, (len(path) > 0,))


def row_values_to_maze_values(rows):
    dmz = DefaultMazeValue
    vals = {
        # dmz.FILLER: dmz.HORIZONTAL_PATH,
        dmz.WALL.value: dmz.WALL,
        dmz.HORIZONTAL_PATH.value: dmz.HORIZONTAL_PATH,
        dmz.VERTICAL_PATH.value: dmz.VERTICAL_PATH,
    }
    for i, row in enumerate(rows):
        row = [vals[v] for v in row if v in vals]
        rows[i] = row


if __name__ == "__main__":
    main()
