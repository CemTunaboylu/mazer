from enum import Enum
import random
from typing import Tuple, Union

from sys import path
from os.path import dirname

path.extend([dirname(__file__), dirname(__file__) + "/.."])

from defaults import DefaultMaze, DefaultMazeValue, show_bits
from dtypes import add, Direction, Vector, directions
from maze import Maze, MazeValue


random.seed(9)


def by_shuffling():
    global directions
    shuff = directions[:]
    random.shuffle(shuff)
    for d in shuff:
        yield d


def by_shuffling_same():
    random.shuffle(directions)  # shuffles in place constantly
    for d in directions:
        yield d


def random_indexing():
    for _ in directions:
        ix = random.randint(0, 1_000_000) % len(directions)
        yield directions[ix]


def random_direction(by):
    yield from by


def is_cell_valid(maze: Maze, cells_coor: Vector):
    """
    we only want to carve passages into untouched cells,
    to avoid creating circular loops in the maze.
    """
    return maze.is_in(cells_coor) and not maze.get_value(cells_coor).is_visited()


def dfs(
    maze_dims: Vector,
    start: Union[Vector],
    maze_value=DefaultMazeValue,
    maze=DefaultMaze,
    debug=False,
) -> Maze:
    space = Maze.create_no_path_space(maze_dims, maze_value.get_unplayable()[0])
    maze = maze(space, maze_value)
    num_unvisited = [maze.num_nodes]

    if debug:
        print(f"[space] : {space}")
        print(f"[num_unvisited] : {num_unvisited}")
        print(f"[start] : {start}")

    def move(frm: Vector, to: Vector, d: Direction) -> Tuple[Vector, Vector]:
        frm_val = maze.get_value(frm)
        to_val = maze.get_value(to)

        frm_val = frm_val.move(d)
        to_val = to_val.move(d.compliment())

        return frm_val, to_val

    def carve_passages_from(coor: Vector, n):
        if 0 >= n[0]:
            return
        if debug:
            print(f"[coor] : {coor}")
        for d in random_direction(by_shuffling()):
            (vec, _) = d.value
            current = add(coor, vec)
            if not is_cell_valid(maze, current):
                if debug:
                    print(f"    cell {current} is not valid")
                continue

            if debug:
                print(f"    [coor] : {coor}")
                print(f"    [d] : {d}")
                print(f"    [current] : {current}")
            f, t = move(coor, current, d)
            if debug:
                print("    [from] : ", show_bits(f))
                print("    [to] : ", show_bits(t))
            maze.set_value(coor, f)
            maze.set_value(current, t)
            n[0] -= 1
            carve_passages_from(current, n)

    carve_passages_from(start, num_unvisited)
    return maze


if __name__ == "__main__":
    from display import *

    def test():
        d = 20
        maze_size = (d, d)
        tile_size = 30
        screen = create_screen(maze_size, tile_size)
        m = dfs(Vector(maze_size))

        draw_space(m.space, screen, tile_size)

        save(screen, "test")

    test()
