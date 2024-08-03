from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Dict, Generator, List

from dtypes import *


# TODO: we can compress the maze into an integer
# TODO: mazes are compressed i.e. when thought as a game scene, one coordinate expands into x boxes.
# TODO: ensure to not intervene with the solution i.e. the shortest path solution
# that the maze is created around should stay as the shortest path.
# TODO: maybe I can create all the solutions of length of_length, and then put 1s
# around the solution, so that the maze is created around the solution.
# TODO: First of all, there should be random obstacles in the maze.


class MazeValue(Enum):
    __metaclass__ = ABCMeta

    # TODO: make this n-dimensional
    def can_play_to(
        self,
        other: "MazeValue",
        dir: Vector,
        *rules_to_pass: Callable[["MazeValue", "MazeValue"], bool],
    ) -> bool:
        unplayables = set(self.get_unplayable())
        if self in unplayables:
            return False
        if other in unplayables:
            return False
        return all(rule(self, other) for rule in rules_to_pass)

    @staticmethod
    @abstractmethod
    def get_playable() -> Tuple:
        pass

    @staticmethod
    @abstractmethod
    def get_unplayable() -> Tuple:
        pass


class MetaMaze(type):
    __metaclass__ = ABCMeta
    maze_types: Dict[str, type] = {}
    required_attributes_for_maze = ["space", "playable", "dims", "num_nodes"]

    def __init__(cls, cls_name, cls_bases, cls_dict):
        # super(MetaMaze, cls).__init__(cls_name, cls_bases, cls_dict)
        if not MazeBase in cls_bases:
            MetaMaze.maze_types[cls_name] = cls

    def __call__(self, *args, **kwargs):
        make = kwargs.get("make", "")
        obj = MetaMaze.maze_types.get(make, None)
        if not obj:
            if not self.__class__.__name__ in MetaMaze.maze_types:
                new_class = MetaMaze(make, (GenericMaze,), {})
                globals()[make] = new_class
                obj = new_class(*args, **kwargs)
            else:
                obj = super(MetaMaze, self).__call__(*args, **kwargs)
        else:
            for required_attr in MetaMaze.required_attributes_for_maze:
                # if there is not such attribute, force it :)
                if not getattr(self, required_attr, None):
                    setattr(self, required_attr, None)
                    # print(f"'{required_attr}' is injected to '{make}' - {MetaMaze}")
        return obj


class MazeBase(object):
    pass


# TODO: implement an iterator
class Maze(MazeBase):
    __metaclass__ = MetaMaze

    def __init__(self, **kwargs):
        self.__metaclass__.__call__(self, **kwargs)
        for name, value in kwargs.items():
            setattr(self, name, value)

    @abstractmethod
    def __repr__(self):
        return "<%s>" % self.description

    @property
    def description(self):
        return f"{self.__dict__}"

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __move_in_dims(self, coordinate: Vector):
        slc = self.space
        for c in coordinate:
            slc = slc[c]
        return slc

    def get_value(self, coordinate: Vector) -> MazeValue:
        return self.__move_in_dims(coordinate)

    def set_value(self, coordinate: Vector, to: MazeValue):
        slc = self.__move_in_dims(coordinate[:-1])
        slc[coordinate[-1]] = to

    def __reduce(self, function, initial):
        space = self.space
        a = initial

        while (isinstance(space, list) or isinstance(space, str)) and len(space) > 1:
            a = function(a, space)
            space = space[0]

        return a

    def dim(self) -> List[int]:
        if self.dims:
            return self.dims
        self.dims = self.__reduce(lambda acc, iterable: acc + [len(iterable)], [])
        return self.dims

    def num_nodes_in(self) -> int:
        if self.num_nodes:
            return self.nums
        self.num_nodes = self.__reduce(lambda acc, iterable: acc * len(iterable), 1)
        return self.num_nodes

    def num_walkable_nodes(self) -> int:
        space = self.space
        stack = [space]
        num = 0
        while stack and isinstance(space, list):
            if isinstance(space[0], list):
                stack.extend([s for s in space])
            elif isinstance(space[0], str):
                num += sum(space[0].count(p.value) for p in self.playable)
            else:
                num += sum(space.count(p) for p in self.playable)
            space = stack.pop()

        return num

    def is_in(self, coordinate: Vector) -> bool:
        return all(0 <= coor_p < dim for (coor_p, dim) in zip(coordinate, self.dims))

    def is_playable(self, coordinate: Vector) -> bool:
        return self.get_value(coordinate) in self.playable

    def can_play_from(self, frm: Vector, to: Vector, dir: Vector) -> bool:
        f, t = self.get_value(frm), self.get_value(to)
        return f.can_play_to(t, dir)

    @staticmethod
    def default_neighbor_shifts_for(
        dim: int,
        can_move_diagonally: bool = False,
        dirs: List[int] = [-1, 1],  # possible directions for each dimension
    ) -> Generator[Vector, None, None]:

        # TODO: implement this
        if can_move_diagonally:
            pass

        # orthogonal movement only
        for d in range(dim):
            for i in dirs:
                n = [0] * dim
                n[d] = i
                yield Vector(n)

    # TODO: assumes that curr and prev positions only differ in 1 dimension
    # and connects the path between them
    # TODO: make this more generic to n-dimensional path connect with a vector
    def set_path(self, curr, prev, to=1):
        maze = self.space
        diff_axis = [i for i, (dc, dp) in enumerate(zip(curr, prev)) if dc != dp]
        if not diff_axis:
            return
        diff_axis = diff_axis[0]
        indices = [curr[diff_axis], prev[diff_axis]]
        indices.sort()

        for r in range(indices[1] - indices[0] + 1):
            coors = prev[:diff_axis] + [indices[0] + r] + prev[diff_axis + 1 :]
            self.set_value(coors, to)

    @staticmethod
    def create_no_path_space(
        lengths_of_axis: Vector,
        wall_value: MazeValue,
        dimensionality: int = 2,
    ):
        if len(lengths_of_axis) == 1:
            lengths_of_axis = lengths_of_axis * dimensionality  # square

        # TODO: I can implement copy-on-write for this to save space
        space = [wall_value] * lengths_of_axis[-1]
        for l in lengths_of_axis[:-1]:
            space = [space[:] for r in range(l)]
        return space


class GenericMaze(Maze):
    def __init__(self, **kwargs):
        kwargs["make"] = self.__class__.__name__
        super(GenericMaze, self).__init__(**kwargs)
