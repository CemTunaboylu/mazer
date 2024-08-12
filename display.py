from typing import Tuple

import pygame
from dtypes import mul


def right_wall_params(x, y, tile_size) -> tuple:
    x += tile_size
    return (x, y), (x, y + tile_size)


def left_wall_params(x, y, tile_size) -> tuple:
    return (x, y + tile_size), (x, y)


def bottom_wall_params(x, y, tile_size) -> tuple:
    y += tile_size
    return (x + tile_size, y), (x, y)


def top_wall_params(x, y, tile_size) -> tuple:
    return (x + tile_size, y), (x, y)


def draw(self, coors, sc, tile, debug=False, path=None):
    x, y = mul(coors, tuple([tile] * len(coors)))
    draw_params = [
        right_wall_params,
        left_wall_params,
        bottom_wall_params,
        top_wall_params,
    ]
    v = self.value
    # TODO: make this a separate method
    if debug and path and coors in path:
        number_font = pygame.font.SysFont(None, 16)  # Default font, Size 16
        number_image = number_font.render("X", True, pygame.color.Color(0, 0, 255))
        sc.blit(number_image, (x + 5, y + 5))
    # TODO: make this a method and take it as a parameter
    for c in range(0, 4):  # 1 means there is passage
        val_at_bit = 1 << c
        i = v & val_at_bit
        if i:  # if there is passage, do not draw a wall
            continue
        pygame.draw.line(
            sc,
            pygame.Color("darkgreen"),
            *draw_params[c](x, y, tile),
        )


def create_screen(maze_size: Tuple[int, int], tile_size=30):
    pygame.init()
    pygame.font.init()
    w_size = mul(maze_size, tuple([tile_size] * len(maze_size)))
    screen = pygame.display.set_mode(w_size)
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((255, 255, 255))
    return screen


def draw_space(space, screen, tile_size=30, debug=False, path=None):
    [
        draw(v, (x, y), screen, tile_size, debug=debug, path=path)
        for (y, r) in enumerate(space)
        for (x, v) in enumerate(r)
    ]


def save(screen, jpg_name: str = "test"):
    pygame.display.update()
    pygame.image.save(screen, f"{jpg_name}.jpg")
