from typing import Dict, NewType, List, Tuple

from fibheap import *

from dtypes import *
from defaults import add


# TODO: we can compress the maze into an integer
# TODO: mazes are compressed i.e. when thought as a game scene, one coordinate expands into x boxes.
def create_empty_maze(by: Position, empty=False) -> List[List[bool]]:
    assert len(by) in [1, 2]
    if len(by) == 1:
        by = by * 2  # square
    return [[empty] * by[1] for r in range(by[0])]


def set_col(maze: List[List[bool]], col: int, value: bool, indices=None):
    if not indices:  # set the whole
        indices = [0, len(maze)]

    indices.sort()
    start = indices[0]
    for r in range(indices[1] - indices[0] + 1):
        maze[start + r][col] = value


def set_row(maze: List[List[bool]], row: int, value: bool, indices=None):
    if not indices:  # set the whole
        indices = [0, len(maze[0])]
    indices.sort()
    start = indices[0]
    for r in range(indices[1] - indices[0] + 1):
        maze[row][start + r] = value


# TODO: this should be dynamic for n dimensions
def set_path(curr, prev, maze):
    setters = [set_row, set_col]
    for x in [0, 1]:
        if curr[x] != prev[x]:
            continue
        o = 1 - x
        setters[x](maze, prev[x], 1, [prev[o], curr[o]])
        break


# TODO: ensure to not intervene with the solution i.e. the shortest path solution
# that the maze is created around should stay as the shortest path.


# TODO: maybe I can create all the solutions of length of_length, and then put 1s
# around the solution, so that the maze is created around the solution.


# TODO: First of all, there should be random obstacles in the maze.


"""
# TOOD: implement djikstra and a*, reconstruction of the path
def reconstruct_path(
    best_from: Dict[Position, Position], start: Position, end: Position
):
    pass
"""
