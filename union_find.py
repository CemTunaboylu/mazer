from typing import List


class DisjointSet:
    def __init__(
        self, size: int, parents: List[int] = [], ranks: List[int] = []
    ) -> None:
        self.size = size
        self.ranks = ranks if ranks else [1] * size
        self.parents = parents if parents else list(range(size))

    def __is_elm_valid(self, elm: int) -> bool:
        return self.size > elm and elm >= 0

    def find(self, elm: int) -> int:
        assert self.__is_elm_valid(elm)
        # its own parents
        if self.parents[elm] == elm:
            return elm

        # compress path
        self.parents[elm] = self.find(self.parents[elm])

        return self.parents[elm]

    def union(self, a: int, b: int):
        assert self.__is_elm_valid(a)
        assert self.__is_elm_valid(b)
        # assume that parents of a is of higher rank
        par_high = self.find(a)
        par_low = self.find(b)

        if par_high == par_low:
            return

        # if assumption is wrong, swap
        if self.ranks[par_high] < self.ranks[par_low]:
            par_high, par_low = par_low, par_high

        self.parents[par_low] = par_high
        self.ranks[par_high] += self.ranks[par_low]

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return f"\n\tp:{self.parents}\n\tr:{self.ranks}"
