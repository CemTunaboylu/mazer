from typing import List
from unittest import TestCase, main

from colors import bcolors, color_text
from dtypes import Position
from defaults import DefaultMazeValue, add, show_path
from test_helpers import debug_mode, ignore
from traversal import djikstra, num_walkable_nodes


def create_tensor_with(
    dims: List[int], values: List[DefaultMazeValue] = [DefaultMazeValue.WALL]
):
    if 1 == len(dims):
        return [values[d % len(values)] for d in range(dims[0])]

    return [create_tensor_with(dims[1:], values) for _ in range(dims[0])]


maze_values = [DefaultMazeValue.WALL, DefaultMazeValue.get_playable()]


def create_tensor_with_playable_columns(dims: List[int], cols: List[int]):
    if 1 == len(dims):
        return [maze_values[d in cols] for d in range(dims[0])]

    return [create_tensor_with_playable_columns(dims[1:], cols) for _ in range(dims[0])]


class TestTraversal(TestCase):
    @ignore
    def test_create_tensor_with(self):
        test_cases = [
            ([1, 1], [DefaultMazeValue.WALL]),
            ([1, 1], [DefaultMazeValue.get_playable()]),
            ([2, 2], [DefaultMazeValue.WALL]),
            ([2, 2], [DefaultMazeValue.get_playable()]),
            ([3, 3], [DefaultMazeValue.WALL, DefaultMazeValue.get_playable()]),
            ([3, 3, 3], [DefaultMazeValue.WALL, DefaultMazeValue.get_playable()]),
            ([3, 3, 4], [DefaultMazeValue.WALL, DefaultMazeValue.get_playable()]),
        ]

        if debug_mode:
            from pprint import pprint

        for dims, values in test_cases:
            t = create_tensor_with(dims, values)

            L = len(dims) - 1
            for i, d in enumerate(dims):
                if debug_mode and len(t) != d:
                    print(f"{dims}")
                    pprint(t)
                    print(f"d:{d}")
                self.assertEqual(len(t), d)
                if i < L:
                    t = t[0]
                    continue
                l = (L + 1) // len(values) + 1
                exp_vals = values * l
                self.assertEqual(t, exp_vals[: len(t)])

    @ignore
    def test_num_walkable_nodes(self):
        test_cases = [
            ([1, 1], [DefaultMazeValue.WALL], 0),
            ([1, 1], [DefaultMazeValue.get_playable()], 1),
            ([2, 2], [DefaultMazeValue.WALL], 0),
            ([2, 2], [DefaultMazeValue.get_playable()], 4),
            ([3, 3], [DefaultMazeValue.WALL, DefaultMazeValue.get_playable()], 3),
            ([3, 3, 3], [DefaultMazeValue.WALL, DefaultMazeValue.get_playable()], 9),
            (
                [3, 3, 4],
                [DefaultMazeValue.WALL, DefaultMazeValue.get_playable()],
                2 * 9,
            ),
        ]

        for dims, values, exp_walkable in test_cases:
            maze = create_tensor_with(dims, values)
            walkable = num_walkable_nodes(maze, DefaultMazeValue.get_playable())
            if debug_mode and exp_walkable != walkable:
                from pprint import pprint

                pprint(maze)
                print(f"walkable: {walkable}")
            self.assertEqual(exp_walkable, walkable)

    def test_djikstra(self):
        test_cases = [
            (
                [
                    [DefaultMazeValue.get_playable(), DefaultMazeValue.WALL],
                    [DefaultMazeValue.WALL, DefaultMazeValue.WALL],
                    [DefaultMazeValue.WALL, DefaultMazeValue.get_playable()],
                ],
                (),
            ),
        ]

        start, end = (0, 0), (2, 2)

        for maze, path in test_cases:
            if debug_mode:
                print("maze:")
                [print(m) for m in maze]
            path = djikstra(maze, start, end, debug_mode=debug_mode)
            self.assertEqual(path, None)

        dims = [4, 4]
        t = create_tensor_with_playable_columns(dims, [0, 3])
        start, end = (0, 0), add(dims, (-1, -1))
        for r in range(len(t)):
            copy = t[:]
            copy[r] = [DefaultMazeValue.get_playable()] * len(t[0])

            path = djikstra(copy, start, end, debug_mode=debug_mode)
            if debug_mode:
                print("maze:")
                show_path(copy, path)
            self.assertEqual(len(path), len(copy) + len(copy[0]) - 1)


if __name__ == "__main__":
    from sys import argv

    old_debug_mode = debug_mode

    if len(argv) > 1:
        debug_mode = argv[-1].lower() in ["debug", "1"]
        del argv[:-1]
    else:
        debug_mode = False
    main()

    debug_mode = old_debug_mode
