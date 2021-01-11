
import pygame
from sprite import ShitFromFile

#scolor = (0,255,0)

snakes = {}
snake = None
dificolty = 1

def color_replace(surface, find_color, replace_color):
    s = surface # surface.copy()
    for x in range(s.get_size()[0]):
        for y in range(s.get_size()[1]):
            if s.get_at([x, y]) == find_color:
                s.set_at([x, y], replace_color)
    return s


def setColor(color):
    for i in range(len(snake)):
        for x in range(snake[i].get_size()[0]):
            for y in range(snake[i].get_size()[1]):
                if snakes['gsnake'][i].get_at([x, y]) == (0,255,0):
                    snake[i].set_at([x, y], color)

def load():
    for f in ['gsnake', 'rsnake', 'bsnake']:
        snakes[f] = ShitFromFile(f + '.png', 2, 2)

    global dificolty
    dificolty = 3

    global snake
    snake = [i.copy() for i in snakes['gsnake']]
    setColor((255,0,255))
