import math
import numpy
import pygame

from Permanent import *


def draw_dashed_line(screen, color, start_pos, end_pos, width=1, dash_length=10):
    """ Draw a dashed line in a given screen.
    :param screen: screen that the line will be drawn on.
    :type screen: pygame.display
    :param color: string that represent the color of the line.
    :type color: string
    :param start_pos: tuple that represent the start position (x, y) of the line.
    :type start_pos: tuple
    :param end_pos: tuple that represent the end position (x, y) of the line.
    :type end_pos: tuple
    :param width: the width of the line, default 1.
    :type width: integer
    :param dash_length: the length of a single dash, default 10.
    :type dash_length: integer
    :return: None
    """
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if x1 == x2:
        y_cords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        x_cords = [x1] * len(y_cords)
    elif y1 == y2:
        x_cords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        y_cords = [y1] * len(x_cords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        x_cords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        y_cords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_cords = list(zip(x_cords[1::2], y_cords[1::2]))
    last_cords = list(zip(x_cords[0::2], y_cords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_cords, last_cords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(screen, color, start, end, width)


def message_to_screen(screen, text, text_size, text_color, pos, is_paragraph=False):
    """ This function write a text onto a screen.
    :param screen: screen that the text will be written on.
    :type screen: pygame.display
    :param text: string that represent the text that will be written on the screen.
    :type text: string
    :param text_size: integer that size of the text's font.
    :type text_size: integer
    :param text_color: string that represent the color of the text.
    :type text_color: string
    :param pos: tuple that represent the must left up corner the text will start be written from (x, y).
    :type pos: tuple
    :param is_paragraph: boolean that represent if the text is multi-line or not.
    :type is_paragraph: boolean
    :return: None
    """
    if is_paragraph:
        my_list = text.split("\n")
        n = -1
        for text in my_list:
            n += 1
            chosen_font = pygame.font.Font(MY_FONT, text_size)
            text = chosen_font.render(text, 1, text_color)
            screen.blit(text, (pos[0], pos[1] + n * text_size))
    else:
        chosen_font = pygame.font.Font(MY_FONT, text_size)
        text = chosen_font.render(text, 1, text_color)
        screen.blit(text, pos)
