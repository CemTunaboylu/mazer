from typing import List
from unittest import TestCase, main

from colors import bcolors
from dtypes import add
from defaults import DefaultMaze, DefaultMazeValue, color_path
from test_helpers import ignore, debug
from traversal import djikstra


def create_tensor_with(
    dims: List[int], values: List[DefaultMazeValue] = [DefaultMazeValue.WALL]
):
    if 1 == len(dims):
        return [values[d % len(values)] for d in range(dims[0])]

    return [create_tensor_with(dims[1:], values) for _ in range(dims[0])]


maze_values = [DefaultMazeValue.WALL, DefaultMazeValue.VERTICAL_PATH]


def create_tensor_with_playable_columns(dims: List[int], cols: List[int]):
    if 1 == len(dims):
        return [maze_values[d in cols] for d in range(dims[0])]

    return [create_tensor_with_playable_columns(dims[1:], cols) for _ in range(dims[0])]


class TestTraversal(TestCase):
    debug_mode = False
    debug_logs = []

    def __debug(self):
        if self.debug_mode:
            for log in self.debug_logs:
                print(log)
            print("-" * 100)

        self.debug_logs.clear()

    def log(self, *args, **kwargs):
        self.debug_logs.append(*args, **kwargs)

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

        for dims, values in test_cases:
            t = create_tensor_with(dims, values)

            L = len(dims) - 1
            for i, d in enumerate(dims):
                try:
                    self.log(f"{dims}")
                    self.log(t)
                    self.log(f"d:{d}")

                    self.assertEqual(len(t), d)
                except AssertionError as e:
                    print(e)
                    self.fail()
                self.__debug()
                if i < L:
                    t = t[0]
                    continue
                l = (L + 1) // len(values) + 1
                exp_vals = values * l
                try:
                    self.assertEqual(t, exp_vals[: len(t)])
                except AssertionError as e:
                    print(e)
                    self.fail()

    def test_num_walkable_nodes(self):
        test_cases = [
            ([1, 1], [DefaultMazeValue.WALL], 0),
            ([1, 1], [DefaultMazeValue.get_playable()[0]], 1),
            ([2, 2], [DefaultMazeValue.WALL], 0),
            ([2, 2], [DefaultMazeValue.get_playable()[0]], 4),
            ([3, 3], [DefaultMazeValue.WALL, DefaultMazeValue.get_playable()[0]], 3),
            ([3, 3, 3], [DefaultMazeValue.WALL, DefaultMazeValue.get_playable()[0]], 9),
            (
                [3, 3, 4],
                [DefaultMazeValue.WALL, DefaultMazeValue.get_playable()[0]],
                2 * 9,
            ),
        ]

        for dims, values, exp_walkable in test_cases:
            space = create_tensor_with(dims, values)
            maze = DefaultMaze(space)
            walkable = maze.num_walkable_nodes()
            try:
                self.log(f"dims:{dims}, values:{values}")
                self.log(space)
                self.log(f"walkable: {walkable}, exp: {exp_walkable}")
                self.assertEqual(exp_walkable, walkable)
            except AssertionError as e:
                print(e)
                self.fail()
            self.__debug()

    def test_djikstra(self):
        test_cases = [
            (
                [
                    [
                        DefaultMazeValue.get_playable()[0],
                        DefaultMazeValue.get_unplayable()[0],
                    ],
                    [
                        DefaultMazeValue.get_unplayable()[0],
                        DefaultMazeValue.get_unplayable()[0],
                    ],
                    [
                        DefaultMazeValue.get_unplayable()[0],
                        DefaultMazeValue.get_playable()[0],
                    ],
                ],
                (),
            ),
        ]

        start, end = (0, 0), (2, 2)

        for space, path in test_cases:
            self.log(space)
            maze = DefaultMaze(space)
            path = djikstra(maze, start, end)
            try:
                self.assertEqual(path, None)
            except AssertionError as e:
                print(e)
                djikstra(maze, start, end, debug_mode=self.debug_mode)
            self.__debug()

        dims = [4, 4]
        t = create_tensor_with_playable_columns(dims, [0, 3])
        start, end = (0, 0), add(dims, (-1, -1))
        for r in range(len(space)):
            copy = t[:]
            maze = DefaultMaze(copy)
            copy[r] = [DefaultMazeValue.get_playable()[0]] * len(t[0])

            path = djikstra(maze, start, end)
            self.log(color_path(maze, path, color=bcolors.FAIL))
            try:
                self.assertEqual(len(path), len(copy) + len(copy[0]) - 1)
            except (AssertionError, TypeError) as e:
                print(e)
                path = djikstra(
                    maze, start, end, debug_mode=self.debug_mode
                )  # do it again with logs
            self.__debug()


if __name__ == "__main__":
    main()
