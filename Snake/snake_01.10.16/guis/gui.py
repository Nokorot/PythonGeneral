import pygame
from pygame.locals import *

import os, sys
sys.path.insert(0, os.path.abspath('../utils'))

from Colors import *
from util import fromBounds, sum

from button import *
from textfield import *
from glider import Glider

class Gui:

    def __init__(self, bounds):
        self.x, self.y, self.width, self.height = fromBounds(bounds)

        self.xcenter = self.x + self.width/2
        self.ycenter = self.y + self.height/2

        self.selected = 0
        self.comps = []

    def select(self, comp):
        self.comps[self.selected].selected = False
        if type(comp) == int:
            self.selected = comp
        else:
            self.selected = self.comps.index(comp)
        self.comps[self.selected].selected = True


    def update(self):
        index = 0
        for c in self.comps:
            c.selected = (self.selected == index)
            c.update()
            index += 1

    def render(self, screen):
        for c in self.comps:
            c.render(screen)

    def eventCathcer(self, event):
        for c in self.comps:
            if c.eventCathcer(event):
                break

        if event.type == pygame.KEYDOWN:
            if [K_TAB, K_RIGHT, K_DOWN].__contains__(event.key):
                self.selected = (self.selected + 1) % len(self.comps)
            if [K_LEFT, K_UP].__contains__(event.key):
                self.selected = (self.selected - 1) % len(self.comps)

    def bounds(self):
        return self.x, self.y, self.width, self.height

    def addComponent(self, component, index=None):
        component.parent = self
        if not index:
            self.comps.append(component)
        else:
            self.comps.insert(component, index)

    def getGrid(self, X, Y, space):
        return Grid(self.bounds(), X, Y, space)

class Rectangle:

    def __init__(self, bounds):
        self.x, self.y, self.width, self.height = fromBounds(bounds)

    def moveto(self, x, y, center=False, centerx=False, centery=False):
        if center or centerx:   self.x = x - self.width/2.
        else:                   self.x = x
        if center or centery:   self.y = y - self.height/2.
        else:                   self.y = y

    def getPos(self):
        return self.x, self.y

    def getSize(self):
        return self.width, self.height

    def contains(self, point):
        return \
            point[0] > self.x and point[0] < self.x + self.width and \
            point[1] > self.y and point[1] < self.y + self.height

    def pgRect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))

    def corners(self):
        x, y = self.x, self.y
        width, height = self.width, self.height
        return [(x,y), (x+width-1,y), (x+width-1, y+height-1), (x, y+height-1)]

    def subRec(self, x, y, w, h):
        ax = self.x + self.width * x
        ay = self.y + self.height * y
        aw = self.width * w
        ah = self.height * h
        return Rectangle((ax, ay, aw, ah))

class Grid:

    def __init__(self, bounds, X, Y, space):
        self.x, self.y, self.width, self.height = fromBounds(bounds)
        self.space = space
        self.X = X
        self.Y = Y

    def getRect(self, x, y):
        X, Y, space = self.X, self.Y, self.space

        if type(X) == int:
            width = float(self.width) / X
            xp = self.x + width * x
        elif [list, tuple].__contains__(type(X)):
            width = float(self.width) * X[x] / sum(X)
            xp = self.x + float(self.width) * sum(X, 0, x)/sum(X)

        if type(Y) == int:
            height = float(self.height) / Y
            yp = self.y + height * y
        elif [list, tuple].__contains__(type(Y)):
            height = float(self.height) * Y[y] / sum(Y)
            yp = self.y + float(self.height) * sum(Y, 0, y)/sum(Y)

        rect = Rectangle((xp + space / 2.0, yp + space / 2.0, width - space, height - space))
        return rect
