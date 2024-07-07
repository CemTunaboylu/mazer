from typing import Dict, List, Set, Tuple, Union
from collections import defaultdict

from fibheap import makefheap, fheappush, fheappop

from dtypes import Maze, MazeValue, Position
from defaults import (
    add,
    DefaultMazeValue,
    default_neighbor_shifts_for,
    get_value,
)


def num_nodes_in(maze: Maze) -> int:
    n = 1
    while not isinstance(maze, list):
        n *= len(maze)
        maze = maze[0]

    return n


def dim(maze: Maze) -> List[int]:
    dims = []
    while isinstance(maze, list):
        dims.append(len(maze))
        maze = maze[0]

    return dims


def num_walkable_nodes(
    maze: Maze, playable: MazeValue = DefaultMazeValue.get_playable()
) -> int:
    if isinstance(maze, list) and not isinstance(maze[0], list):
        return maze.count(playable)

    # TODO: make this non-recursive
    return sum(num_walkable_nodes(m, playable) for m in maze)


# TODO: implement a maze class to facilitate this i.e. num. of walkable nodes
# in a dimension
def djikstra(
    maze: Maze,
    start: Position,
    target: Union[Position, None] = None,
    default_distance=float("inf"),
    debug_mode: bool = False,
    walkable_maze_value=DefaultMazeValue.get_playable(),
) -> Union[List[Position] | None]:
    # return inf if we didn't record its distance to start yet, trying to shrink the memory footprint
    distances: Dict[Position, Tuple[int, Position]] = defaultdict(
        lambda: (default_distance, None)
    )

    distances[start] = (0, start)

    dims = dim(maze)
    is_in_borders = lambda pos: all(
        0 <= coor_p < dim for (coor_p, dim) in zip(pos, dims)
    )
    is_playable = lambda p: get_value(maze, p) == walkable_maze_value

    # do not count the walls
    # TODO: if there are less than shortest manhattan distance or whatever the distance calc. method is
    # given, we can stop immediately without traversing the maze
    num_of_walkable_nodes = num_walkable_nodes(maze)

    pri_que = makefheap()
    fheappush(pri_que, (0, start))

    path = None
    if debug_mode:
        print(f"distances: {distances}")
        print(f"dims: {dims}")
        print(f"num_of_walkable_nodes: {num_of_walkable_nodes}")
        print(f"priority queue: {pri_que}")
        print(f"path: {path}")

    # visited checks -> fib heap will be changing prios thus will always have at most num_nodes
    # node in it, thus emptying it corresponds to the visiting all walkable nodes
    # additionally, unless we come up with a better path to a node - with less cost -, we don't put it
    # in the fib heap thus it acts as a visited check
    while pri_que.num_nodes:
        cost, current = fheappop(pri_que)
        if target is not None and current == target:
            path = reconstruct_path_between(start, target, distances)
            break
        for n in default_neighbor_shifts_for(len(dims)):
            neighbor_cell = add(current, n)
            if not is_in_borders(neighbor_cell) or not is_playable(neighbor_cell):
                continue
            n_cost = cost + 1
            known_distance = distances[neighbor_cell][0]
            in_fib_heap = known_distance != default_distance
            if known_distance <= n_cost:
                continue
            distances[neighbor_cell] = (n_cost, current)
            if in_fib_heap:
                # throws exception if n_cost > known_distance but we check that beforehand
                pri_que.decrease_key(neighbor_cell, n_cost)
            else:
                fheappush(pri_que, (n_cost, neighbor_cell))

    if debug_mode:
        print(f"{'-' * 100}")
        print(f"distances: {distances}")
        print(f"priority queue: {pri_que}")
        print(f"path: {path}")

    return path


def reconstruct_path_between(
    start: Position,
    end: Position,
    distances: Dict[Position, Tuple[int, Position]],
) -> List[Position]:
    path = []
    current = end
    while current != start:
        path.append(current)
        # TODO: this should not happen but handle it
        if not current in distances:
            raise Exception(f"no path from {start} to {end}")
        current = distances[current][1]

    path.append(start)
    path.reverse()
    return path


if __name__ == "__main__":
    djikstra(None, None, None)
