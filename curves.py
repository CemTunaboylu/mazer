from sys import argv
from typing import List, Tuple

from colors import color_values_of
from defaults import DefaultMaze, DefaultMazeValue
from dtypes import Position
from gray import gray_code_of
from maze import *


# TODO: can use the non-recursive method here with gray codes
positions = [
    (0, 0),
    (0, 1),
    (1, 1),
    (1, 0),
]

functions = [
    lambda x, y, n: (y, x),
    lambda x, y, n: (x, y + n),
    lambda x, y, n: (x + n, y + n),
    lambda x, y, n: (n - 1 - y + n, n - 1 - x),
]


def hindex_to_2d(hindex: int, N: int) -> Tuple[int, int]:
    last_2_bits = lambda h: h & 3
    (x, y) = positions[last_2_bits(hindex)]

    hindex = hindex >> 2

    n = 4
    while n <= N:
        n2 = n // 2
        x, y = functions[last_2_bits(hindex)](x, y, n2)
        hindex = hindex >> 2
        n *= 2

    return (x, y)


if __name__ == "__main__":
    N: int = 0
    debug = False
    if len(argv) > 1:
        debug = any(a.lower() in {"debug", "d"} for a in argv[1:])
        to_int = lambda a: int(a[a.index("n") + 1 :])
        N = [to_int(a) for a in argv[1:] if "n" in a][0]

    if not N:
        N = int(input("maze dimensions: "))

    prev, curr = ([0, 0]), None
    points = []

    maze_dim = N * 2 - 1

    space = Maze.create_no_path_space([maze_dim], DefaultMazeValue.WALL)
    maze = DefaultMaze(space)

    playable = DefaultMazeValue.FILLER

    for i in range(N * N):
        (c, r) = hindex_to_2d(i, N)
        points.append((r, c))
        # stretch the maze
        r, c = r * 2, c * 2
        space[r][c] = playable
        curr = [r, c]
        maze.set_path(curr, prev, playable)
        prev = curr

    space.reverse()

    if debug:
        print([(c, i) for i, c in enumerate(points)])

    [print(color_values_of(row, playable)) for row in maze.space]
