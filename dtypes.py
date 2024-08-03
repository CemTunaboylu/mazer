from operator import add as add_op
from operator import sub as sub_op
from operator import eq as eq_op

from typing import Callable, NewType, Tuple, Union

Number = Union[float, int]
Vector = NewType("Vector", Tuple[int, ...])


# Order can matter for the pos and other
def __operate_on(
    op: Callable[[Number, Number], Number],
    pos: Vector,
    other: Vector,
) -> Vector:
    # TODO: hold each position as a generator if dimensions are big?
    return Vector(tuple(op(p, o) for p, o in zip(pos, other)))


def add(pos: Vector, other: Vector) -> Vector:  # Generator[int, None, None]:
    return __operate_on(add_op, pos, other)


def sub(pos: Vector, other: Vector) -> Vector:  # Generator[int, None, None]:
    return __operate_on(sub_op, pos, other)


def eq(pos: Vector, other: Vector) -> bool:
    return all(__operate_on(eq_op, pos, other))
