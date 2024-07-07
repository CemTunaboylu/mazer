debug_mode = True


def ignore(f):
    return lambda n: None


def toggle_debug(t_obj):
    debug_mode = not debug_mode
    return t_obj
