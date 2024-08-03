from re import I
from unittest import TestCase
from typing import Any, List


class BaseTest(TestCase):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.debug_mode = False
        self.debug_logs: List[Any] = []

    def debug(self):
        if self.debug_mode:
            for log in self.debug_logs:
                print(log)
            print("-" * 100)

        self.debug_logs.clear()

    def log(self, *args, **kwargs):
        self.debug_logs.append(*args, **kwargs)

    def logged_assert(self, test, assertion, args):
        fail = False
        try:
            assertion(*args)
        except Exception as e:
            fail = True
            self.log(e)
        if not fail:
            return
        defer = None
        if not self.debug_mode:
            old = self.debug_mode
            defer = lambda: self.debug_mode == old
            self.debug_mode = True
        self.debug()
        if defer:
            defer()
        test.fail()
