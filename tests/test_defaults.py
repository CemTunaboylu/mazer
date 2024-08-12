from unittest import main

from base_test import BaseTest
from defaults import DefaultMazeValue, extend_dfs_maze_value_with
from dtypes import Direction


class TestDefaults(BaseTest):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def test_custom_rules_for_can_play_to(self):
        extend_dfs_maze_value_with()
        dmv = DefaultMazeValue
        l = list(dmv.__iter__())
        play = l[-1]  # playable to all directions
        normally_playable = (play, play, Direction.U)
        for rule_return in [True, False]:
            frm, to, dir = normally_playable
            r = frm.can_play_to(
                to, dir, lambda a, b: rule_return, lambda a, b: rule_return
            )
            self.assertEqual(rule_return, r)


if __name__ == "__main__":
    main()
