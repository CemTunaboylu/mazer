from unittest import main

from base_test import BaseTest
from curves import hindex_to_2d
from test_helpers import ignore


class TestCurves(BaseTest):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def test_hindex_to_2d_n_equals_2(self):
        exps = [(0, 0), (0, 1), (1, 1), (1, 0)]
        N = 2
        for i, e in enumerate(exps):
            h_res = hindex_to_2d(i, N)
            self.assertEqual(
                hindex_to_2d(i, N), e, f"point:{i}, h_res:{h_res}, exp:{e}, N:{N}"
            )

    def test_hindex_to_2d_n_equals_4(self):
        N = 4
        exps = [
            (0, 0),  # 0
            (1, 0),  # 1
            (1, 1),  # 2
            (0, 1),  # 3
            (0, 2),  # 4
            (0, 3),  # 5
            (1, 3),  # 6
            (1, 2),  # 7
            (2, 2),  # 8
            (2, 3),  # 9
            (3, 3),  # 10
            (3, 2),  # 11
            (3, 1),  # 12
            (2, 1),  # 13
            (2, 0),  # 14
            (3, 0),  # 15
        ]
        i = 2
        e = exps[i]
        for i, e in enumerate(exps):
            h_res = hindex_to_2d(i, N)
            self.assertEqual(h_res, e, f"point:{i}, h_res:{h_res}, exp:{e}, N:{N}")


if __name__ == "__main__":
    main()
