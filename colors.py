class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def color_text(text: str, color: str = bcolors.OKGREEN, bold: bool = False) -> str:
    return f"{bcolors.BOLD if bold else ''}{color}{text}{bcolors.ENDC}"


def color_values_of(iterable, val_to_color):
    clr = lambda v: color_text(str(v), bold=True) if v == val_to_color else str(v)
    return " ".join([clr(i) for i in iterable])
