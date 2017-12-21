
import pygame
from pygame import *

from entity import Application, Entity
from vec import *
from Colors import *
from sprite import SpriteFromFile, ShitFromFile
from gui import Rectangle
from button import Button

from serverClient import GameClient

from math import sqrt
import random

import time

from main import *

def MakeNewGame(mainMenu, gameId):
    game = Game(mainMenu, gameId)
    game.serverClient.make(game.level.levelSize)
    game.chooseColor(int(game.serverClient.playerId)+1)
    return game

def ConnectToGame(mainMenu, gameId):
    game = Game(mainMenu, gameId)
    print game.myColor
    game.serverClient.connect()
    game.chooseColor(int(game.serverClient.playerId)+1)
    return game

class Game(Application):
    def __init__(self, mainMenu, gameId):
        Application.__init__(self, mainMenu)
        self.bg = SpriteFromFile('bg 0.jpg')
        self.bg.transform(size=self.bg.scale('fill', ScreenSize/4))

        self.level = Level(self)
        self.add(self.level)

        self.myColor = -1
        self.whoesTurn = -1;

        ###
        self.applyB = Button(Rectangle((ScreenWidth - 150, 50, 100, 50)), 'Apply')
        self.applyB.action = lambda x: self.applyMove()
        self.add(self.applyB)
        ###

        self.selectedStone = None
        self.pathStone = None
        self.path = []

        self.serverClient = GameClient(mainMenu.serverClient, self, gameId)

    def Update(self):
        pass

    def Render(self, screen, pos):
        for i in range(4):
            for j in range(4):
                self.bg.draw(screen, ScreenSize / 4 * Vec(i, j), center=False)
        for t in self.path:
            screen.circle(red, t.getPos(), t.space * 0.4)

    def EventAction(self, event):
        '''if (event.type == pygame.MOUSEBUTTONDOWN):
            if self.selectedStone != None:
                for stone in self.level.stones'''
        if (event.type == pygame.MOUSEBUTTONUP):
            if self.selectedStone != None:
                tile = self.level.getClosestTile(Vec(pygame.mouse.get_pos()))
                if tile != None:
                    if self.path.__contains__(tile):
                        self.selectedStone.setTile(tile)
                        self.path = self.path[: self.path.index(tile)+1]
                    if self.level.legalMove(self.selectedStone.tile.cord, tile.cord, self.selectedStone != self.pathStone or len(self.path) <= 1):
                        self.selectedStone.setTile(tile)
                        self.path.append(tile)
                self.selectedStone.selected = False
                self.selectedStone = None

        if (event.type == pygame.KEYDOWN):
            if [K_RETURN, K_SPACE].__contains__(event.key):
                self.applyMove()

    def chooseColor(self, color):
        self.myColor = color
        self.serverClient.setColor(self.myColor)

    def selectStone(self, stone):
        # TODO: Is it my turn ...
        if stone != self.pathStone:
            if self.pathStone != None:
                self.pathStone.setTile(self.path[0])
            self.pathStone = stone
            self.path = [stone.tile]

        if self.selectedStone != None:
            self.selectedStone.selected = False
        self.selectedStone = stone
        stone.selected = True

    def applyMove(self):
        if self.pathStone == None or len(self.path) <= 1:
            return
        self.pathStone.tile = self.path[0]
        self.path[0].stone = self.pathStone
        print self.serverClient.move(self.path)
        self.pathStone = None
        self.path = []
        self.whoesTurn = (self.whoesTurn + 1) % 6

class Level(Entity):

    def __init__(self, game):
        Entity.__init__(self,  ScreenSize / 2)#* Vec(0.4, 0.5))
        self.game = game
        self.size = Vec(0.75, 0.75) * ScreenWidth

        self.tiles = {}
        self.stones = []
        self.constructLevel(3)

        self.time = 0;

    def addColor(self, color):
        for tile in self.tiles[color]:
            stone = Stone(color, self)
            self.add(stone)
            self.stones.append(stone)
            stone.setTile(tile);

    def removeColor(self, color):
        for tile in self.tiles.itervalues():
            if tile.stone.color == color:
                self.stones.remove(tile.stone)
                tile.stone.removeMe()
                tile.stone = None

    def cords2Pos(self, x, y):
        from math import pi, cos, sin
        xa = x + 0.5 * y
        ya = y * sqrt(3)/2
        n = 1-self.game.myColor
        s, c = sin(pi * n / 3), cos(pi * n / 3)
        xa, ya = c * xa - s * ya, s * xa + c * ya

        '''
        xa = self.cord[0] * sqrt(3)/2
        ya = self.cord[1] + 0.5 * self.cord[0]
        '''
        return xa * self.tileSpace, ya * self.tileSpace

    def constructLevel(self, levelSize):
        self.levelSize = ls = levelSize
        a = self.size / ((ls*3+1) + 0.3)
        self.tileSpace = min(a[0] , a[1]*sqrt(3)/2)

        self.cords = []
        def addTile(x, y, color):
            if not self.cords.__contains__([x,y]):
                self.cords.append([x,y])
                tile = Tile(self, (x,y), color)
                self.add(tile)
                if not self.tiles.__contains__(color):
                    self.tiles[color] = []
                self.tiles[color].append(tile)

        def makeCorner(x0, y0, xd, yd, color):
            for y in range(ls):
                for x in range(y+1):
                    xa = x0 + xd[0] * y + yd[0] * x
                    ya = y0 + xd[1] * y + yd[1] * x
                    addTile(xa, ya, color)

        makeCorner( -ls, 2*ls, (0, -1), (1,0),  1)
        makeCorner( -2*ls, ls, (1, 0), (0,-1),  2)
        makeCorner(-ls,-ls,    (1,0), (-1, 1),  3)
        makeCorner( ls, -2*ls, (0, 1),  (-1,0), 4)
        makeCorner( 2*ls, -ls, (-1, 0), (0,1),  5)
        makeCorner( ls, ls,    (-1, 0), (1,-1), 6)

        for y in range((ls*3+1)):
            for x in range(y+1):
                addTile(-x + ls,y- 2*ls, 0)
        self.cords = sorted(self.cords)

        self.grid = []
        import numpy as np
        for x in set(np.array(self.cords)[:,0]):
            T = filter(lambda h: h[0] == x, self.cords)
            T = np.array(T)[:,1]
            self.grid.append((x, min(T), x, max(T)))

    def legalMove(self, a, b, firstMove):
        print a, b
        if a == b or self.getTileByCord(b).stone != None:
            return False
        diag = 1 if a[0] == b[0] else 2 if a[1] == b[1] else 3 if a[0]+a[1] == b[0]+b[1] else 0
        if diag != 0:
            mx, my, l = max(a[0], b[0]), min(a[1], b[1]), max(abs(a[0]-b[0]), abs(a[1]-b[1]))
            if l == 1:
                return firstMove
            if l % 2 == 0:
                for t in range(1, l):
                    if diag == 1:
                        tile = self.getTileByCord((a[0], my+t))
                    if diag == 2:
                        tile = self.getTileByCord((mx-t, a[1]))
                    if diag == 3:
                        tile = self.getTileByCord((mx-t, my+t))
                    if (t == l/2 and tile.stone == None) or (t != l/2 and tile.stone != None):
                        return False
                return True
        return False;

    def Update(self):
        pass

    def Render(self, screen, pos):
        def calcPos(x, y):
            xa, ya = self.cords2Pos(x,y)
            return xa + self.getPos()[0], ya + self.getPos()[1]

        c = (255, 255, 255)
        for l in self.grid:
            screen.line(c, calcPos(l[0], l[1]),       calcPos(l[2], l[3]),       2)
            screen.line(c, calcPos(l[0]+l[1], -l[1]), calcPos(l[2]+l[3], -l[3]), 2)
            screen.line(c, calcPos(l[1], l[0]),       calcPos(l[3], l[2]),       2)

    def getClosestTile(self, pos):
        for tileL in self.tiles.itervalues():
            for tile in tileL:
                if (pos - tile.getPos()).norm() < (tile.space * 0.4):
                    return tile
        return None

    def getTileByCord(self, cord):
        for tileL in self.tiles.itervalues():
            for tile in tileL:
                if tile.cord == cord:
                    return tile
        return None

Colors = [black, red, blue, green, purple, cyan, pink]
class Tile(Entity):

    def __init__(self, level, cord, color):
        self.cord = cord
        self.space = level.tileSpace
        self.level = level
        self.color = color
        Entity.__init__( self, None )
        self.stone = None

    def getPos(self):
        xa, ya = self.level.cords2Pos(*self.cord)
        #xa = self.cord[0] + 0.5 * self.cord[1]
        #ya = self.cord[1] * sqrt(3)/2
        '''
        xa = self.cord[0] * sqrt(3)/2
        ya = self.cord[1] + 0.5 * self.cord[0]
        '''
        return Vec(xa, ya) + self.parent.getPos()

    def Update(self):
        pass

    def Render(self, screen, pos):
        screen.circle(Colors[self.color], self.getPos(), self.space * 0.1)

class Stone(Entity):

    def __init__(self, color, level):
        Entity.__init__( self, Vec(0,0))
        self.sprite = SpriteFromFile('grad.png')
        self.sprite.transform(True, size= Vec2(level.tileSpace * 0.8))

        self.game = level.game
        self.color = color
        self.tile = None
        self.selected = False

    def setTile(self, tile):
        if self.tile != None:
            self.tile.stone = None
        self.tile = tile
        tile.stone = self

    def getPos(self):
        if self.selected:
            return self.pos
        if self.tile == None:
            return Vec(0,0)
        return self.tile.getPos()

    def Render(self, screen, pos):
        if self.tile != None:
            #self.sprite.draw(screen, self.getPos())
            screen.circle(Colors[self.color], self.getPos(), self.tile.space * 0.3)

    def Update(self):
        if self.selected:
            self.pos = Vec(pygame.mouse.get_pos())

    def eventAction(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN):
            d = (Vec(event.pos) - self.getPos())
            if d.norm() <= self.tile.space * 0.3:
                self.game.selectStone(self)
                '''self.selected = True
                self.parent.selectedStone = self'''
