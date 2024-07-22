from unittest import TestCase


class BaseTest(TestCase):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.debug_mode = False
        self.debug_logs = []

    def debug(self):
        if self.debug_mode:
            for log in self.debug_logs:
                print(log)
            print("-" * 100)

        self.debug_logs.clear()

    def log(self, *args, **kwargs):
        self.debug_logs.append(*args, **kwargs)

    def logged_assert(self, test, assertion, args):
        try:
            assertion(*args)
        except Exception as e:
            self.log(e)
            self.debug()
            test.fail()
