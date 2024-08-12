from sys import argv
from typing import List, Tuple

from styles import color_values_of
from defaults import DefaultMaze, DefaultMazeValue
from display import visual, FILLER, WALL
from dtypes import Vector, vec_to_dir
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


def hilbert_space(dims: Vector, playable=FILLER):
    assert 1 == len(set(dims))  # for now ensure that it is nxn
    prev, curr = ([0, 0]), None
    points = []

    space = Maze.create_no_path_space(dims, DefaultMazeValue.get_unplayable()[0])
    maze = DefaultMaze(space)

    N = dims[0] * dims[1]

    for i in range(N):
        # TODO: dims[0] is not correct here
        (c, r) = hindex_to_2d(i, dims[0])
        points.append((r, c))

        curr = [r, c]
        diff = sub(curr, prev)
        dir = vec_to_dir(diff)
        if dir:
            space[r][c] = space[r][c].move(dir)
            space[prev[0]][prev[1]] = space[prev[0]][prev[1]].move(dir.compliment())
        # maze.set_path(curr, prev, playable)
        prev = curr

    return maze, points


if __name__ == "__main__":
    N: int = 0
    debug = False
    if len(argv) > 1:
        debug = any(a.lower() in {"debug", "d"} for a in argv[1:])
        to_int = lambda a: int(a[a.index("n") + 1 :])
        N = [to_int(a) for a in argv[1:] if "n" in a][0]

    if not N:
        N = int(input("maze dimensions: "))

    # for i in range(N * N):
    #     (c, r) = hindex_to_2d(i, N)
    playable = FILLER
    maze, points = hilbert_space(Vector((N, N)), playable)
    maze.space.reverse()
    if debug:
        print([(c, i) for i, c in enumerate(points)])

    [print(color_values_of(row, playable)) for row in maze.space]
