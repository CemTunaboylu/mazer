debug_mode = False


def ignore(f):
    return lambda n: None


def debug(t_func):
    def f(self):
        self.debug_mode = not self.debug_mode
        t_func(self)
        self.debug_mode = not self.debug_mode

    return f
