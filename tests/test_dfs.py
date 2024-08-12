from unittest import main

from base_test import BaseTest
from dtypes import Vector, sub
from defaults import Direction, extend_dfs_maze_value_with
from display import create_screen, draw_space, save
from generators.dfs import dfs
from traversal import djikstra
from test_helpers import debug


class TestDfs(BaseTest):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.debug_mode = True

    def test_dfs_is_fully_connected(self):
        test_cases = [(3, 7), (7, 3), (15, 15), (20, 20), (28, 28)]
        extend_dfs_maze_value_with()
        for i, dims in enumerate(test_cases):
            maze = dfs(dims, Vector((0, 0)))
            self.log([str(r) for r in maze.space])

            start = (0, 0)
            target = sub(dims, (1, 1))

            path = djikstra(
                maze,
                Vector(start),
                Vector(target),
            )

            if self.debug_mode:
                tile_size = 30
                # tiles = [tile_size] * len(dims)
                path = [(p[1], p[0]) for p in path]
                # self.log(f"{i} path: {path}")

                screen = create_screen(dims, tile_size=tile_size)
                draw_space(maze.space, screen, tile_size, self.debug_mode, set(path))
                save(screen, f"tests/test_{i}")

            self.logged_assert(self, self.assertIsNotNone, (path,))
            self.logged_assert(self, self.assertTrue, (len(path) > 0,))


if __name__ == "__main__":
    main()
