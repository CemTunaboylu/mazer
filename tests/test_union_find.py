from unittest import main

from base_test import BaseTest
from generators.union_find import DisjointSet


class TestDisjointSet(BaseTest):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def test_find_no_compression(self):
        test_cases = [
            # parents
            list(range(3)),
            [0] * 3,
            [0, 0, 2],
        ]

        for parents in test_cases:
            disjoint_set = DisjointSet(len(parents), parents)

            for i, p in enumerate(parents):
                result = disjoint_set.find(i)
                self.assertEqual(p, result, f"[{i}] {result}!={p} for {parents}")

    def test_find_with_compression(self):
        test_cases = [
            # parents, expected
            ([0, 0, 1], [0, 0, 0]),  # 2 will first compress to 0,
            ([0, 2, 0], [0, 0, 0]),  # 1 will first compress to 0,
        ]

        for parents, expected in test_cases:
            disjoint_set = DisjointSet(len(parents), parents)

            for i in range(disjoint_set.size):
                result = disjoint_set.find(i)
                exp = expected[i]
                self.assertEqual(exp, result, f"[{i}] {result}!={exp} for {parents}")

    def test_compression_of_find(self):
        test_cases = [
            # parents, find_queries, parents list for each query, expected parent
            (
                [0, 0, 1, 2, 3],
                range(5),
                (
                    (
                        [0, 0, 1, 2, 3],
                        [0, 0, 1, 2, 3],
                        [0, 0, 0, 2, 3],
                        [0, 0, 0, 0, 3],
                        [0, 0, 0, 0, 0],
                    )
                ),
                [0] * 5,
            ),
            (
                [0, 0, 1, 2, 3],
                range(4, -1, -1),  # find from reverse will compress all at once
                (
                    (
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                    )
                ),
                [0] * 5,
            ),
        ]

        for parents, find_queries, parents_transformation, expected in test_cases:
            disjoint_set = DisjointSet(len(parents), parents)

            for i, q in enumerate(find_queries):
                result = disjoint_set.find(q)
                pars = disjoint_set.parents
                pt = parents_transformation[i]
                self.assertEqual(
                    pars,
                    pt,
                    f"[{i}] - parent transformation did not match {pars}!={pt}",
                )
                exp = expected[i]
                self.assertEqual(
                    result,
                    exp,
                    f"[{i}] - find result did not match {exp}!={result}",
                )

    def test_union(self):
        test_cases = [
            # target_parents, union_queries, parents and ranks list for each query, expected parent
            (
                ((0, 1), (1, 2), (2, 3), (3, 4)),  # note that order matters
                (
                    ([0, 0, 2, 3, 4], [2, 1, 1, 1, 1]),
                    ([0, 0, 0, 3, 4], [3, 1, 1, 1, 1]),
                    ([0, 0, 0, 0, 4], [4, 1, 1, 1, 1]),
                    ([0, 0, 0, 0, 0], [5, 1, 1, 1, 1]),
                ),
                [0] * 5,
            ),
            (
                (
                    (4, 3),
                    (1, 0),
                    (3, 2),
                    (2, 1),
                ),  # proving the orders importance
                (
                    ([0, 1, 2, 4, 4], [1, 1, 1, 1, 2]),
                    ([1, 1, 2, 4, 4], [1, 2, 1, 1, 2]),
                    ([1, 1, 4, 4, 4], [1, 2, 1, 1, 3]),
                    ([1, 4, 4, 4, 4], [1, 2, 1, 1, 5]),
                ),
                [1, 4, 4, 4, 4],
            ),
        ]

        for (
            union_queries,
            parents_ranks_transformation,
            expected_parents,
        ) in test_cases:
            disjoint_set = DisjointSet(len(expected_parents))

            for i, q in enumerate(union_queries):
                disjoint_set.union(*q)
                parents_and_ranks = disjoint_set.parents, disjoint_set.ranks
                exp_parents_and_ranks = parents_ranks_transformation[i]
                for exp, got in zip(exp_parents_and_ranks, parents_and_ranks):
                    self.assertListEqual(
                        exp,
                        got,
                        f"[{i}] - query:{q}, {exp}!={got}",
                    )
            self.assertListEqual(
                expected_parents,
                disjoint_set.parents,
                f"  parents did not match {expected_parents} != {disjoint_set.parents}",
            )


if __name__ == "__main__":
    main()
