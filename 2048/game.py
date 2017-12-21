
from entity import *
from vec import *
from Colors import *
from sprite import SpriteFromFile, ShitFromFile

import random

from main import *

class Game(Aplication):

    def __init__(self):
        self.level = Level()
        Aplication.__init__(self)
        self.add(self.level)

class Level(Entity):

    def __init__(self):
        Entity.__init__(self,  ScreenSize / 2)
        self.size = Vec(500, 500)

        self.levelSize = IVec(4, 4)
        self.tileSize = self.size / self.levelSize

        self.tiles = [None for _ in range(self.levelSize[0] * self.levelSize[1])]
        self.grid = [(Vec(x, y) + 0.5) * self.tileSize - self.size * 0.5 \
                                    for y in range(self.levelSize[0]) \
                                    for x in range(self.levelSize[1])]

        self.addTile()
        self.time = 0;

    def move(self, dir):
        if self.time > 0: return
        self.time = 5

        w, h = self.levelSize;

        def index(x, y, i):
            if (dir == 'Left'):
                if (x - i < 0): return -1
                return (x - i) + y * w
            if (dir == 'Right'):
                if (w-1 - x + i >= w): return -1
                return (w-1 - x + i) + y * w
            if (dir == 'Down'):
                if (h-1 - y + i >= h): return -1
                return x + (h-1 - y + i) * w
            if (dir == 'Up'):
                if (y - i < 0): return -1;
                return x + (y - i) * w

        tileMoved = False
        for x in range(w):
            for y in range(h):
                thisTile = self.tiles[index(x, y, 0)]
                if (thisTile != None):
                    i = 0
                    while (index(x, y, i+1) >= 0):
                        if (self.tiles[index(x, y, i+1)] == None):
                            i+=1
                        elif (self.tiles[index(x, y, i+1)].value == thisTile.value):
                            thisTile.setValue(thisTile.value * 2)
                            self.tiles[index(x, y, i+1)].removeMe()
                            i+=1; break;
                        else:
                            break;
                    if (i != 0):
                        tileMoved = True
                        self.tiles[index(x, y, i)] = self.tiles[index(x,y,0)]
                        self.tiles[index(x,y,0)] = None;
                        self.tiles[index(x, y, i)].moveTo(self.grid[index(x,y,i)])
        if (tileMoved):
            self.addTile()

    def addTile(self, rand=-1):
        if rand==-1:
            free = []

            index = 0;
            for tile in self.tiles:
                if (tile == None):
                    free.append(index)
                index+=1

            if len(free) < 1:
                print 'GAME OVER'
                return

            rand = random.choice(free)

        self.tiles[rand] = Tile(self, self.grid[rand])

    def Update(self):
        if (self.time > 0):
            self.time -= 1
            if (self.time < 0):
                self.time = 0

    def Render(self, screen, pos):
        screen.rect(light_gray, makeRect(self.getPos(), self.size*0.99, True))

        for loc in self.grid:
            screen.rect(black, makeRect(loc+self.getPos(), self.tileSize, True), 5)

    def eventAction(self, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT):
                self.move('Left')
            elif (event.key == pygame.K_RIGHT):
                self.move('Right')
            elif (event.key == pygame.K_UP):
                self.move('Up')
            elif (event.key == pygame.K_DOWN):
                self.move('Down')

class Tile(Entity):

    def __init__(self, level, pos):
        Entity.__init__( self, pos)
        self.Colors = [red, blue, green, purple, cyan, pink, deep_pink,
                        soft_brown, darkcyan, skyblue, wheat, silver, goldenrod]

        self.size = level.tileSize

        level.add(self)

        self.newPos = self.pos
        self.moveSpeed = self.size * 0.5;

        if (random.randint(0, 9) == 0):
            self.setValue(4)
        else:
            self.setValue(2)

    def moveTo(self, pos):
        self.newPos = pos

    def setValue(self, value):
        self.value = value
        font = pygame.font.SysFont("monospace", 60)
        self.labelS = Vec(font.size(str(value)));
        self.label = font.render(str(value), 1, white)

    def Update(self):
        if (self.pos != self.newPos):
            delta = (self.newPos - self.pos)
            if (delta > self.moveSpeed):
                self.pos = self.pos + delta.normalize() * self.moveSpeed;
            else:
                self.pos = self.newPos

    def Render(self, screen, pos):
        from math import log
        screen.rect( self.Colors[int(log(self.value) / log(2)) - 1], makeRect(self.getPos() , self.size*0.9, True) )
        screen.screen.blit(self.label, (self.getPos() - self.labelS/2).asTuple())
