import pygame
from pygame.locals import *

from Colors import *
from entity import Entity

class Component(Entity):
    aColor = (20, 20, 20)
    bColor = gray
    fColor = white
    sColor = white

    def __init__(self, rect, name=''):
        Entity.__init__(self, rect.getPos())
        self.rect = rect
        self.name = name

        self.parent = None

        self.selected = False
        self.selectable = True

    def renderSelected(self):
        pass
