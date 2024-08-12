import argparse

from display import pretty_print
from dtypes import sub, Vector
from traversal import djikstra


def hilbert(dimensions):
    from generators.curves import hilbert_space, visual

    maze, points = hilbert_space(dimensions)
    return maze


def eller(dimensions):
    from generators.eller import ellers_algorithm

    maze = ellers_algorithm(dimensions)
    return maze


def dfs(dimensions):
    from generators.dfs import dfs
    from defaults import extend_dfs_maze_value_with

    extend_dfs_maze_value_with()
    maze = dfs(dimensions, Vector((0, 0)))
    return maze


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Mazer",
        description="Creates mazes programmatically",
    )
    parser.add_argument(
        "dimensions",
        metavar="D",
        type=int,
        nargs="*",
        default=[16, 16],
        help="dimensions [x,y,z,...]",
    )
    # algorithms = ["dfs", "eller", "hilbert"]
    algorithms = ["dfs"]
    parser.add_argument(
        "algo", type=str, nargs="*", choices=algorithms, default=algorithms[0]
    )
    # parser.add_argument("-t", "--terminal", action="store_true")
    parser.add_argument("-s", "--save", action="store_true")
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="runs all of the algorithms to create mazes",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="runs debug",
    )

    args = parser.parse_args()
    if args.all:
        args.algo = algorithms

    print(args, args.dimensions, args.verbose)
    g = globals()

    for a in args.algo:
        print(f"Creating with {a}")
        al = g.get(a, None)
        if al:
            maze = al(args.dimensions)
            start = Vector((0, 0))
            target = Vector(sub(args.dimensions, (1, 1)))
            path = djikstra(maze, start, target)
            path = [(p[1], p[0]) for p in path]
            # if args.terminal:
            #     pr = pretty_print(maze.space)
            #     print(pr)
        if args.save:
            from display import *

            tile_size = 30
            screen = create_screen(args.dimensions, tile_size)
            draw_space(maze.space, screen, tile_size, path=set(path))
            save(screen, f"test-{a}-{args.dimensions}")
