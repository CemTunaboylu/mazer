from enum import Enum
from operator import add as add_op
from operator import sub as sub_op
from operator import mul as mul_op
from operator import eq as eq_op

from typing import Callable, NewType, Tuple

Number = int
Vector = NewType("Vector", Tuple[Number, ...])


class Direction(Enum):
    # <U> <D> <L> <R>
    U = (Vector((0, -1)), 1 << 3)
    D = (Vector((0, 1)), 1 << 2)
    L = (Vector((-1, 0)), 1 << 1)
    R = (Vector((1, 0)), 1)

    # returns the opposite bit
    def compliment(self):
        m = 2
        if 0 > self.value[0][0] or 0 > self.value[0][1]:
            m = 1 / 2

        return int(self.value[1] * m)

    def get_vec(self):
        return self.value[0]

    def get_bit(self):
        return self.value[1]


def vec_to_dir(diff) -> Direction:
    d = None
    muld = sum(mul(diff, [1, 2]))
    # 2, -2, -1, 1
    corr = [Direction.R, Direction.D, Direction.U, Direction.L]
    return corr[muld]


directions = list(Direction.__iter__())


# Order can matter for the pos and other
def __operate_on(
    op: Callable[[Number, Number], Number],
    pos: Vector,
    other: Vector,
) -> Vector:
    # TODO: hold each position as a generator if dimensions are big?
    return Vector(tuple(op(p, o) for p, o in zip(pos, other)))


def add(pos, other):  # Generator[int, None, None]:
    return __operate_on(add_op, pos, other)


def sub(pos, other):  # Generator[int, None, None]:
    return __operate_on(sub_op, pos, other)


def mul(pos, other):  # Generator[int, None, None]:
    return __operate_on(mul_op, pos, other)


def eq(pos, other) -> bool:
    return all(__operate_on(eq_op, pos, other))
