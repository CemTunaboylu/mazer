from re import S
from typing import Callable, DefaultDict, Dict, List, Set, Tuple
from random import randint, seed
from collections import defaultdict

from maze import MazeValue
from union_find import DisjointSet
from styles import underline
from dtypes import Position, SymbolSet


class EllerMazeValue(MazeValue):
    WALL = "|"
    FULL_PATH = " "
    HORIZONTAL_PATH = "_"
    FILLER = "‧"
    SEPARATOR = " "

    @staticmethod
    def get_playable() -> Tuple:
        return (EllerMazeValue.FULL_PATH, EllerMazeValue.HORIZONTAL_PATH)

    @staticmethod
    def get_unplayable() -> Tuple:
        return (EllerMazeValue.WALL,)

    def can_play_to(
        self,
        other: MazeValue,
        dir: Position,
        *rules_to_pass: Callable[[MazeValue, MazeValue], bool],
    ) -> bool:

        can_move_down = lambda s, o: not (
            1 == dir[0] and self == EllerMazeValue.HORIZONTAL_PATH
        )
        can_move_up = lambda s, o: not (
            -1 == dir[0] and other == EllerMazeValue.HORIZONTAL_PATH
        )
        rules = (can_move_down, can_move_up, *rules_to_pass)
        return super().can_play_to(other, dir, *rules)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


EllerSymbols: DefaultDict[str, str] = defaultdict(lambda: "")
EllerSymbols.update(
    {
        "passable": " ",
        "horizontal_passable": "_",
        "separator": "|",
        "unplayable": "|",
    }
)


seed(9)
NUM_CELLS_TO_MERGE_IN_ROW = lambda r: r // 2
NUM_VERTICALS_TO_MERGE_IN_COL = (1, 2)

# TODO: randint(NUM_CELLS_TO_MERGE_IN_ROW(num_rows)) can randomize


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


def merge_cells_to_the_right_randomly(dset: DisjointSet, should_merge=P_x(50)):
    # merge cells in the same row randomly (to the right)
    num_cols = len(dset)
    # left to right ensures that the set owner is the left most element
    for to_merge in range(num_cols - 1):
        if not should_merge(randint(0, 1_000_000)):
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
            r = randint(0, diff * 1_000_000)
            p = r % diff
            verticals.add(w_start + p)
        w_start = x + 1
    return verticals


# maze_dims = [y,x] , [z,y,x]
# TODO: you may want to make this a generator
# TODO: make this n-dimensional
def ellers_algorithm(
    maze_dims: Tuple[int, ...],
    debug: bool = False,
    assertions: List[Callable[..., bool]] = [
        lambda m_dims: len(m_dims) == 2
    ],  # TODO: for now, we support 2d only
) -> List[str]:
    for a in assertions:
        assert a(maze_dims)
    num_cols, num_rows = maze_dims[-1], maze_dims[0]
    rows = []
    dset = DisjointSet(num_cols)
    for _ in range(num_rows):
        merge_cells_to_the_right_randomly(dset)
        verticals = open_vertical_passages_for_each_region(dset)
        rows.append(convert_to_row(dset, verticals, debug=debug))
        reuse_disjoint_set(dset, verticals)

    # make the last row
    reuse_disjoint_set(dset, verticals)
    dset.parents = [1] * (len(rows[-1]))  # remove horizontal walls
    rows.append(convert_to_row(dset, set()))
    return rows


def __symbols(
    dset: DisjointSet,
    verticals: Set[int],
    x: int,
    other: int,
    decide_cell: Callable[[bool, int], str],
    decide_add: Callable[[bool, str], str],
    symbol_set: DefaultDict[str, str],
):
    set_x = dset.find(x)
    set_next = dset.find(other)
    cell_x = decide_cell(x in verticals, set_x)
    add = symbol_set.get("separator")
    if set_x == set_next:
        add = decide_add(other in verticals, cell_x)
    return [cell_x, add]


def prepare_symbols(
    dset: DisjointSet,
    verticals: Set[int],
    x: int,
    other: int,
    symbol_set: DefaultDict[str, str] = EllerSymbols,
):
    def decide_cell(b: bool, _: int) -> str:
        return (
            symbol_set.get("passable") if b else symbol_set.get("horizontal_passable")
        )

    decide_add = lambda b, cell_x: symbol_set.get("passable") if b else cell_x
    return __symbols(
        dset,
        verticals,
        x,
        other,
        decide_cell=decide_cell,
        decide_add=decide_add,
        symbol_set=symbol_set,
    )


def prepare_debug_symbols(
    dset: DisjointSet,
    verticals: Set[int],
    x: int,
    other: int,
    symbol_set: DefaultDict[str, str] = EllerSymbols,
):
    from string import ascii_lowercase

    def decide_cell(b: bool, set_x: int) -> str:
        s_set_x = ascii_lowercase[set_x]
        return s_set_x if b else underline(s_set_x)

    decide_add = lambda b, s_set_x: s_set_x if b else underline(s_set_x)

    return __symbols(
        dset,
        verticals,
        x,
        other,
        decide_cell=decide_cell,
        decide_add=decide_add,
        symbol_set=symbol_set,
    )


def convert_to_row(dset: DisjointSet, verticals: Set[int], debug=False):
    row = ["|"]
    for x in range(len(dset) - 1):  # move left to right
        args = (dset, verticals, x, x + 1)
        symbols = prepare_symbols(*args) if not debug else prepare_debug_symbols(*args)
        row.extend(symbols)

    # handle last set
    x = len(dset) - 1
    args = (dset, verticals, x, x - 1)
    last_symbol = prepare_symbols(*args) if not debug else prepare_debug_symbols(*args)
    last_symbol[-1] = "|"
    row.extend(last_symbol)
    return "".join(row)


def pretty_print(
    rows,
    print_col_witdth: bool = False,
    symbol_set: DefaultDict[str, str] = EllerSymbols,
) -> str:
    to_print = []
    L = len(rows[0])
    to_print.append("".join([symbol_set.get("horizontal_passable")] * L))
    if print_col_witdth:
        to_print.extend([str((r, len(r))) for r in rows])
    else:
        to_print.extend([str(r) for r in rows])
    return "\n".join(to_print)
