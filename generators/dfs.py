from enum import Enum
from aenum import extend_enum
import random
from typing import Callable, Tuple, Union

from sys import path
from os.path import dirname

path.extend([dirname(__file__), dirname(__file__) + "/.."])

from defaults import DefaultMaze
from maze import Maze, MazeValue
from dtypes import Vector, add

random.seed(9)

playable = []


class DFSMazeValue(MazeValue):
    # <up_bit> <down_bit> <left_bit> <right_bit>
    NO_MOVE = 0

    def can_play_to(
        self,
        other: MazeValue,
        dir: Vector,
        *rules_to_pass: Callable[[MazeValue, MazeValue], bool],
    ) -> bool:
        def can_move(dir):
            shift = None
            if 1 == dir[0]:  # down
                shift = Direction.S
            elif -1 == dir[0]:  # down
                shift = Direction.N
            elif 1 == dir[1]:  # right
                shift = Direction.E
            elif -1 == dir[1]:  # right
                shift = Direction.W
            else:
                pass
            return lambda x, y: (x.value & shift.value[-1]) and (
                y.value & shift.compliment()
            )

        rules = (can_move(dir), *rules_to_pass)
        return super().can_play_to(other, dir, *rules)

    @staticmethod
    def get_playable():
        global playable
        if not playable:
            playable = list(DFSMazeValue.__iter__())[1:]

        return playable

    def clone(self):
        return self.__class__.__call__(self.value)

    @staticmethod
    def get_unplayable():
        return (DFSMazeValue.NO_MOVE,)

    def is_visited(self):
        return 0 != self.value

    # automatically makes the cell visited since the value is not 0 now
    def move(self, bit: int) -> "DFSMazeValue":
        v = self.value | bit
        return DFSMazeValue(v)

    def __repr__(self) -> str:
        return f"{self.value}"

    def __str__(self) -> str:
        return f"{self.value}"


dmv = DFSMazeValue


class Direction(Enum):
    # <U> <D> <L> <R>
    N = (Vector((-1, 0)), 1 << 3)
    S = (Vector((1, 0)), 1 << 2)
    W = (Vector((0, -1)), 1 << 1)
    E = (Vector((0, 1)), 1)

    def compliment(self):
        m = 2
        if 0 > self.value[0][0] or 0 > self.value[0][1]:
            m = 1 / 2

        return int(self.value[1] * m)


directions = list(Direction.__iter__())


def extend_dfs_maze_value_with_directions():
    global directions

    def get_var_as_str(enm):
        e = str(enm)
        i = e.find(".")
        return e[i + 1 :]

    try:
        for i in range(1, 2 ** len(directions)):
            names = [get_var_as_str(d) for d in directions if (d.value[-1] & i) > 0]
            name = "-".join(names)
            extend_enum(DFSMazeValue, f"{name}", i)
    except Exception as e:
        pass

    DFSMazeValue.get_playable()


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


def dfs(maze_dims: Vector, start: Union[Vector, None] = None, debug=False):
    space = Maze.create_no_path_space(maze_dims, DFSMazeValue.get_unplayable()[0])
    maze = DefaultMaze(space, DFSMazeValue)
    num_unvisited = [maze.num_nodes]
    if not start:
        start = Vector([0] * len(maze.dims))

    if debug:
        print(f"[space] : {space}")
        print(f"[num_unvisited] : {num_unvisited}")
        print(f"[start] : {start}")

    def move(frm: Vector, to: Vector, d: Direction) -> Tuple[Vector, Vector]:
        frm_val = maze.get_value(frm)
        to_val = maze.get_value(to)

        frm_val = frm_val.move(d.value[-1])
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


def show_bits(v):
    if not isinstance(v, int):
        v = v.value
    return bin(v)[2:].zfill(4)


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
