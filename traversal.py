from typing import Dict, List, Set, Tuple, Union
from collections import defaultdict

from fibheap import makefheap, fheappush, fheappop

from dtypes import add, Number, Vector
from maze import Maze, MazeValue

PositionToDistance = Dict[Vector, Tuple[Number, Union[Vector, None]]]


def djikstra(
    maze: Maze,
    start: Vector,
    target: Union[Vector, None] = None,
    default_distance=float("inf"),
    debug_mode: bool = False,
) -> Union[List[Vector] | None]:
    # return inf if we didn't record its distance to start yet, trying to shrink the memory footprint
    distances: PositionToDistance = defaultdict(lambda: (default_distance, None))

    distances[start] = (0, start)

    dims = maze.dim()
    path = None

    pri_que = makefheap()
    fheappush(pri_que, (0, start))

    if debug_mode:
        print(f"distances: {distances}")
        print(f"dims: {dims}")
        print(f"priority queue: {pri_que}")

    # visited checks -> fib heap will be changing prios thus will always have at most num_nodes
    # node in it, emptying it corresponds to the visiting all walkable nodes
    # additionally, unless we come up with a better path to a node - with less cost -, we don't put it
    # in the fib heap thus it acts as a visited check
    while pri_que.num_nodes:
        cost, current = fheappop(pri_que)
        if target is not None and current == target:
            path = reconstruct_path_between(start, target, distances)
            break
        for n in maze.default_neighbor_shifts_for():
            neighbor_cell = add(current, n.get_vec())
            if not maze.is_in(neighbor_cell) or not maze.can_play_from(
                current, neighbor_cell, n
            ):
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
    start: Vector,
    end: Vector,
    distances: Dict[Vector, Tuple[Number, Union[Vector, None]]],
) -> List[Vector]:
    path = []
    current = end
    while current != start:
        path.append(current)
        # TODO: this should not happen but handle it
        if not current in distances:
            raise Exception(f"no path from {start} to {end}")
        _, current = distances[current]

    path.append(start)
    path.reverse()
    return path
