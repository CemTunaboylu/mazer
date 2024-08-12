from collections import defaultdict
from typing import Callable, DefaultDict, List, Set, Tuple, Union

import pygame

from maze import MazeValue
from defaults import DefaultMazeValue
from dtypes import add, mul, Direction
from styles import color_values_of


def bottom_wall_params(x, y, tile_size) -> tuple:
    x += tile_size
    return (x, y), (x, y + tile_size)


def top_wall_params(x, y, tile_size) -> tuple:
    return (x, y + tile_size), (x, y)


def right_wall_params(x, y, tile_size) -> tuple:
    y += tile_size
    return (x + tile_size, y), (x, y)


def left_wall_params(x, y, tile_size) -> tuple:
    return (x + tile_size, y), (x, y)


def gradient_colors_for(len):
    m = max(1, (len // 255) + 1)
    r, g, b = (0, 0, 0)
    for x in range(len):
        if x % m == 0:
            r, g, b = add((r, g, b), (1, 0, 1))
        yield pygame.color.Color(r, g, b, a=120)


def draw(
    self,
    coors,
    sc,
    tile,
    # color=pygame.color.Color(0, 0, 255, 120),
    color_generator,
    debug=False,
    path=None,
):
    x, y = mul(coors, tuple([tile] * len(coors)))
    draw_params = [
        right_wall_params,
        left_wall_params,
        bottom_wall_params,
        top_wall_params,
    ]
    v = self.value
    # TODO: make this a separate method
    if path and coors in path:
        # number_font = pygame.font.SysFont(None, 16)  # Default font, Size 16
        # number_image = number_font.render("X", True, pygame.color.Color(0, 0, 255))
        # sc.blit(number_image, (x + 5, y + 5))
        pygame.draw.rect(sc, next(color_generator), (x, y, tile, tile))
    # TODO: make this a method and take it as a parameter
    for c in range(0, 4):  # 1 means there is passage
        val_at_bit = 1 << c
        i = v & val_at_bit
        if i:  # if there is passage, do not draw a wall
            continue
        pygame.draw.line(
            sc, pygame.Color("darkgreen"), *draw_params[c](x, y, tile), width=2
        )


def create_screen(maze_size: Tuple[int, int], tile_size=30):
    pygame.init()
    pygame.font.init()
    margin = 2
    w_size = add(
        mul(maze_size, tuple([tile_size] * len(maze_size))), tuple([margin] * 2)
    )
    screen = pygame.display.set_mode(w_size)
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((255, 255, 255))
    return screen


def draw_space(space, screen, tile_size=30, debug=False, path=None):
    l = 1
    if path:
        l = len(path)

    generator = gradient_colors_for(l)
    [
        draw(
            v,
            (x, y),
            screen,
            tile_size,
            color_generator=generator,
            debug=debug,
            path=path,
        )
        for (y, r) in enumerate(space)
        for (x, v) in enumerate(r)
    ]


def save(screen, jpg_name: str = "test"):
    pygame.display.update()
    pygame.image.save(screen, f"{jpg_name}.jpg")


WALL = "|"
FULL_PATH = " "
HORIZONTAL_PATH = "_"
FILLER = "‧"
SEPARATOR = " "


def visual(space, playable=FILLER) -> List[str]:
    space.reverse()
    return [color_values_of(row, playable) for row in space]


Symbols: DefaultDict[str, str] = defaultdict(lambda: FILLER)
Symbols.update(
    {
        "passable": FULL_PATH,
        "horizontal_passable": HORIZONTAL_PATH,
        "separator": WALL,
        "unplayable": WALL,
    }
)


def prepare_symbols(
    x: int,
    symbol_set: DefaultDict[str, str] = Symbols,
):
    s = [symbol_set.get("passable")] * 2
    if 0 == (x & Direction.D.get_bit()):  # cannot go down
        s[0] = symbol_set.get("horizontal_passable")
    if 0 == (x & Direction.R.get_bit()):  # cannot go right
        s[1] = symbol_set.get("separator")
    return "".join(s)


def pretty_print(
    rows,
    print_col_width: bool = False,
    symbol_set: DefaultDict[str, str] = Symbols,
) -> str:
    to_print = []
    L = len(rows[0]) * 2
    h_passable = symbol_set.get("horizontal_passable")
    separator = symbol_set.get("separator")
    horizontal_wall = "".join([h_passable] * L)
    to_print.append(horizontal_wall)
    for row in rows:
        new_row = [None] * len(row)
        for x, v in enumerate(row):
            new_row[x] = prepare_symbols(v.value)
        new_row.insert(0, separator)
        # if new_row[-1] != separator:
        #     new_row[-1:] = separator
        to_print.append("".join(new_row))
    to_print[-1] = separator + horizontal_wall[1:] + separator
    if print_col_width:
        to_print.extend([str((r, len(r))) for r in rows])
    return "\n".join(to_print)
