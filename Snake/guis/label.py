import pygame
from pygame.locals import *

import os, sys
sys.path.insert(0, os.path.abspath('../utils'))
from Colors import *

from component import Component

def rectField(screen, label):
    rect = label.rect
    if label.bColor:
        pygame.draw.rect(screen, label.bColor, rect.pgRect())
    if pygame.font:
        font = pygame.font.Font(None, int(rect.height))
        t = label.name

        text = font.render(t, 1, label.fColor)
        textpos = text.get_rect(centerx=rect.x + int(rect.width/2), centery= rect.y + int(rect.height/2))
        screen.blit(text, textpos)
    if label.selected:
        lines = rect.corners()
        pygame.draw.lines(screen, red, True, lines)

class Label(Component):
    def __init__(self, rect, name=''):
        Component.__init__(self, rect, name)

        self.bColor = None
        self.draw = rectField

        self.selected = False
        self.selectable = False

        self.time = 0
        self.mark = True
        self.shift = False

    def update(self):
        self.time = (self.time + 1) % 90
        self.mark = self.selected and self.time > 60

    def render(self, screen):
        self.draw(screen, self)
