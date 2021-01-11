
import numpy as np
import pygame
from pygame import K_a, K_s, K_d, K_w, K_SPACE
from quark import qGameObject
from quark.colors import *
from quark.maths import qVec2, qVec
from random import randint

colours = [qRed, qBlue, qLime, qDarkRed, qSilver, qWheat, qDeepOink]
shapes = [
    [qVec(0,0), qVec(0,1), qVec(1,0), qVec(1,1)],
    [qVec(0,-1), qVec(0,0), qVec(1,0), qVec(1,1)],
    [qVec(1,-1), qVec(0,0), qVec(1,0), qVec(0,1)],
    [qVec(0,0), qVec(-1,0), qVec(1,0), qVec(0,1)],
    [qVec(0,-1), qVec(0,0), qVec(0,1), qVec(0,2)],
    [qVec(-1,0), qVec(0,0), qVec(0,1), qVec(0,2)],
    [qVec(1,0), qVec(0,0), qVec(0,1), qVec(0,2)],
]


class Closs(qGameObject):
    def __init__(self, level, pos, clossType):
        self.level = level
        self.type = clossType
        self.shape = shapes[clossType]
        self.pos = pos

        self.moveH = False
        self.fast = False
        self.count = 30

    def Render(self, screen):
        scale = self.level.scale
        ca = self.level.ca
        for a in self.shape:
            r = ca + (self.pos + a)*scale
            screen.rect(colours[self.type], (r[0]+1, r[1]+1, scale-2,scale-2))

    def eventAction(self, event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if [K_a, K_d].__contains__(event.key):
                self.moveH = 1
            if [K_w, K_s].__contains__(event.key):
                def rot(x):
                    if event.key == K_w:
                        return qVec(-x[1], x[0])
                    return qVec(x[1], -x[0])
                shape = map(rot, self.shape)
                if self.isValid(self.pos, shape):
                    self.shape = shape

            if [K_SPACE].__contains__(event.key):
                #self.fast = True
                i = 0
                while self.move():
                    i += 1
                    pass
                print i
                self.place()
        if event.type == pygame.KEYUP:
            if [K_SPACE].__contains__(event.key):
                self.fast = False
            if [K_a, K_d].__contains__(event.key) and not(keys[K_a] or keys[K_d]):
                self.moveH = -1

    def Update(self):
        self.count -= 1;
        self.moveH -= 1;
        if self.count <= 0 or self.fast:
            if not self.move():
                self.place()
            self.count = 15
        keys = pygame.key.get_pressed()
        if self.moveH == 0:
            pp = self.pos + qVec(keys[K_d] - keys[K_a], 0)
            if self.isValid(pp):
                self.pos = pp
            self.moveH = 5

    def place(self):
        self.level.place(self)
        self.removeMe()

    def move(self):
        pp = self.pos + qVec(0,1)
        if self.isValid(pp):
            self.pos = pp
            return True
        return False

    def isValid(self, pos, shape=None):
        if shape == None:
            shape = self.shape
        for ps in [(pos+s).floor() for s in shape]:
            if ps[1] < 0:
                continue
            if ps[1] >= self.level.height or\
                ps[0] >= self.level.width or\
                ps[0] < 0 or\
                self.level.grid[ps[0]+ps[1]*self.level.width] != -1:
                return False
        return True

class Level(qGameObject):
    width = 10
    height = 25
    scale = 22

    def __init__(self):
        self.gameOver = False
        self.grid = np.array([-1 for _ in range(self.width*self.height)])

    def update(self):
        if not self.gameOver:
            qGameObject.update(self)

    def Render(self, screen):
        scale = self.scale;
        cc = screen.center
        self.ca = ca = cc - qVec2(self.width, self.height)*scale / 2.
        self.cb = cb = cc + qVec2(self.width, self.height)*scale / 2.
        for w in range(self.width+1):
            x = ca[0] + w * scale
            screen.line(qCyan, (x, ca[1]), (x, cb[1]))
        for h in range(self.height+1):
            y = ca[1] + h * scale
            screen.line(qCyan, (ca[0], y), (cb[0], y))
        for y in range(self.height):
            for x in range(self.width):
                g = self.grid[y*self.width + x]
                r = ca + qVec2(x,y)*scale
                if g != -1:
                    screen.rect(colours[g], (r[0]+1, r[1]+1, scale-2,scale-2))

    def newPize(self):
        rr = randint(0, 6)
        pos = qVec(self.width/2, -3)
        closs = Closs(self, pos, rr)
        self.add(closs)

    def place(self, closs):
        for s in closs.shape:
            ps = (closs.pos + s).floor()
            if ps[0] + ps[1]*self.width < 0:
                self.gameOver = True
            else:
                self.grid[ps[0] + ps[1]*self.width] = closs.type
        for y in range(self.height):
            if all(self.grid[y*self.width : (y+1)*self.width] != -1):
                for i in range(1,y*self.width):
                    self.grid[(y+1)*self.width-i] = self.grid[y*self.width-i]
        if not self.gameOver:
            self.newPize()
        else:
            print "Game Over"
