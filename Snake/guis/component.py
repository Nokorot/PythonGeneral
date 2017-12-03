import pygame
from pygame.locals import *

import os, sys
sys.path.insert(0, os.path.abspath('../utils'))
from Colors import *

class Component:
    def __init__(self, rect, name=''):
        self.rect = rect
        self.name = name

        self.bColor = gray
        self.fColor = white
        self.sColor = white

        self.parent = None

    def update(self):
        pass

    def render(self, screen):
        pass

    def eventCathcer(self, event):
        return False

    def renderSelected(self):
        pass
