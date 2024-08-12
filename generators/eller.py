from typing import Callable, List, Set, Union
import random

from defaults import DefaultMaze, DefaultMazeValue, merge
from maze import Maze, MazeValue
from generators.union_find import DisjointSet
from styles import underline
from dtypes import Direction, Vector


random.seed(9)
NUM_CELLS_TO_MERGE_IN_ROW = lambda r: r // 2
NUM_VERTICALS_TO_MERGE_IN_COL = (1, 2)


def num_disjoint_sets(dset: DisjointSet) -> int:
    return len(set(dset.parents))


def reuse_disjoint_set(dset: DisjointSet, verticals: Set[int]):
    for x in range(len(dset)):
        # left to right ensures that the set owner is the left most element
        if x in verticals:
            continue  # if there is a vertical, stays the same
        dset.parents[x] = x
        dset.ranks[x] = 1

    # adjust ranks
    s = 0
    while s < len(dset):
        if 1 == dset.ranks[s]:
            s += 1
            continue
        x = s
        while x + 1 < len(dset) and x == dset.parents[x + 1]:
            x += 1
        dset.ranks[s] = x - s + 1
        s = x + 1


P_x = lambda x: lambda r: r > x  # approx. probability of merging
rand_int = lambda d=1: random.randint(0, d * 1_000_000)


def merge_cells_to_the_right_randomly(dset: DisjointSet, should_merge=P_x(50)):
    # merge cells in the same row randomly (to the right)
    num_cols = len(dset)
    # left to right ensures that the set owner is the left most element
    for to_merge in range(num_cols - 1):
        if not should_merge(rand_int()):
            continue
        dset.union(to_merge, to_merge + 1)


def open_vertical_passages_for_each_region(dset: DisjointSet) -> Set[int]:
    verticals: Set[int] = set()
    w_start = 0
    # for each region, have at least 1 vertical passage
    while w_start < len(dset):
        v = dset.parents[w_start]  # get the set owner
        x = w_start
        # find the range of cells that are in the same region [w_start, x)
        while x + 1 < len(dset) and v == dset.parents[x + 1]:
            x += 1
        # randomly generate vertical passages within the region,
        # if by chance the same cell is selected, no problem, it creates variance
        for v in range(*NUM_VERTICALS_TO_MERGE_IN_COL):
            diff = x - w_start + 1
            r = rand_int(diff)
            p = r % diff
            verticals.add(w_start + p)
        w_start = x + 1
    return verticals


# maze_dims = [y,x] , [z,y,x]
# TODO: you may want to make this a generator
# TODO: make this n-dimensional
def ellers_algorithm(
    maze_dims: Vector,
    debug: bool = False,
    maze=DefaultMaze,
    assertions: List[Callable[..., bool]] = [
        lambda m_dims: len(m_dims) == 2
    ],  # TODO: for now, we support 2d only
) -> Maze:
    for a in assertions:
        assert a(maze_dims)
    num_cols, num_rows = maze_dims[-1], maze_dims[0]
    rows = []
    dset = DisjointSet(num_cols)
    for _ in range(num_rows):
        merge_cells_to_the_right_randomly(dset)
        verticals = open_vertical_passages_for_each_region(dset)
        rows.append(convert_to_row(dset, verticals, rows[-1] if rows else None))
        reuse_disjoint_set(dset, verticals)

    # make the last row
    reuse_disjoint_set(dset, verticals)
    dset.parents = [1] * (len(rows[-1]))  # remove horizontal walls
    rows.append(convert_to_row(dset, set(), rows[-1] if rows else None))
    return DefaultMaze(rows)


# TODO: change x and other together
def __passages(
    dset: DisjointSet,
    verticals: Set[int],
    x: int,
    other: int,
    upper_row: Union[List, None],
    default_maze_values=lambda: [DefaultMazeValue.NO_MOVE] * 2,
) -> List[MazeValue]:

    set_x, set_next = dset.find(x), dset.find(other)
    vals = default_maze_values()
    for i, c in enumerate([x, other]):
        if c in verticals:
            vals[i] = vals[i].move(Direction.D)
        if upper_row and (upper_row[c].value & Direction.D.get_bit() > 0):
            vals[i] = vals[i].move(Direction.U)
    if set_x == set_next:
        vals[0] = vals[0].move(Direction.R)
        vals[1] = vals[1].move(Direction.L)

    return vals


def convert_to_row(
    dset: DisjointSet, verticals: Set[int], upper_row: Union[List, None] = None
):
    row = [DefaultMazeValue.NO_MOVE] * len(dset)
    # horizontal checks
    for x in range(len(dset) - 1):  # move left to right
        args = (dset, verticals, x, x + 1, upper_row)
        for i, v in enumerate(__passages(*args)):
            row[x + i] = merge(v, row[x + i])

    return row
