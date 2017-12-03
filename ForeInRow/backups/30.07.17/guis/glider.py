import pygame
from pygame.locals import *

from numpy import linspace

import os, sys
sys.path.insert(0, os.path.abspath('../utils'))
from Colors import *
from util import clamp

from component import Component

def printAction(g):
    print 'Glider %s changed to %f!' % (g.name, g.value())

def lineGlider(screen, g):

    rec = g.rect.subRec(0, 1./3, 1, 1./3)

    pygame.draw.rect(screen, g.bColor, rec.pgRect())

    slimeMarker(screen, g)


def slimeMarker(screen, g):
    pygame.draw.rect(screen, g.fColor, g.markrect.pgRect())


lastV = -1

class Glider(Component):
    def __init__(self, rect, markrect=None, name=''):
        Component.__init__(self, rect, name)

        self.action = printAction
        self.draw = lineGlider
        self.marker = slimeMarker

        if not markrect:
            markrect = rect.subRec(0, 0, 1/16., 1)
        self.markrect = markrect

        self.values = linspace(0, 1, 101)
        self.index = len(self.values) / 2

        self.selected = False

        self.bound = False

    def value(self, index=None):
        if not index:
            index = self.index
        return self.values[index]

    def update(self):
        if self.bound:
            x,y = pygame.mouse.get_pos()
            i = round(len(self.values) * (x - self.rect.x) / self.rect.width)
            self.index = int(clamp(i, 0, len(self.values)-1))


        global lastV
        if not lastV == self.index:
            self.markrect.moveto(self.rect.x + self.rect.width * self.index / (len(self.values)-1), self.rect.y, centerx=True)
            lastV = self.index
            if self.action:
                self.action(self)

    def render(self, screen):
        self.draw(screen, self)
        self.marker(screen, self)

    def eventHandeler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.markrect.contains(event.pos):
                self.bound = True
                return True
        if self.bound and event.type == pygame.MOUSEBUTTONUP:
            self.bound = False

        if event.type == pygame.KEYDOWN:
            if self.selected:
                if event.key == K_RETURN:
                    self.activate()
                    return True

        return False
