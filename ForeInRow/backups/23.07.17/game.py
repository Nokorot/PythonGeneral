
from entity import *
from vec import *
from Colors import *
from sprite import SpriteFromFile, ShitFromFile

import random

from main import *

class FiRGame(Aplication):

    def __init__(self, mainMenu, game, size):
        self.serverClient = mainMenu.serverClient
        ppk = self.serverClient.rsa_packed_public_key
        s_url = 'make::' + game + '::' + ppk + '::' + size
        responce = self.serverClient.request(s_url)

        [key,bord] = responce.split('::')

        self.playerKey = self.serverClient.decrypt(key)


        self.players = [0,0]
        self.level = Level(self)
        Aplication.__init__(self)
        self.add(self.level)

    def eventHandeler(self, event):
        if (event.type == pygame.MOUSEBUTTONUP):
            loc = pygame.mouse.get_pos()
            self.level.addTile(0, loc=loc)

class Level(Entity):

    def __init__(self, game):
        Entity.__init__(self,  ScreenSize / 2)
        self.game = game
        self.size = Vec(700, 500)

        self.levelSize = IVec(7, 5)
        self.tileSize = self.size / self.levelSize

        self.tiles = [None for _ in range(self.levelSize[0] * self.levelSize[1])]
        self.grid = [(Vec(x, y) + 0.5) * self.tileSize - self.size * 0.5 \
                                    for y in range(self.levelSize[1]) \
                                    for x in range(self.levelSize[0])]
                                    
        self.nextColor = 0

    def getTile(self, x, y):
        return self.tiles[x + y * self.levelSize[0]]

    def addTile(self, pos=0, loc=None):
        if loc != None:
            loc = Vec(loc) - self.getPos() + self.size * 0.5
            pos = int(loc[0] / self.size[0] * self.levelSize[0])

        for i in range(self.levelSize[1]):
            if (self.getTile(pos, i) != None):
                if (i == 0): return False
                i -= 1; break

        i = pos + i * self.levelSize[0]

        self.tiles[i] = Tile(self, (self.grid[pos], self.grid[i]), self.nextColor)
        self.nextColor = (self.nextColor + 1) % len(self.game.players)


    def Render(self, screen, pos):
        for loc in self.grid:
            screen.circle(light_gray, tuple((loc + self.getPos()).floor()), 50)

class Tile(Entity):

    def __init__(self, level, pos, color):
        Entity.__init__( self, pos[0])
        self.Colors = [red, blue]
        self.color = color

        self.size = level.tileSize

        level.add(self)

        self.newPos = pos[1]

        self.moveSpeed = self.size * 0.5;

    def Update(self):
        if (self.pos != self.newPos):
            delta = (self.newPos - self.pos)

            if (abs(delta) > self.moveSpeed):
                self.pos = self.pos + delta.normalize() * self.moveSpeed;
            else:
                print 'Hey'
                self.pos = self.newPos

    def Render(self, screen, pos):
        from math import log


        screen.circle(self.Colors[self.color], self.getPos().floor(), 46)

        #screen.rect( self.Colors[int(log(self.value) / log(2)) - 1], #makeRect(self.getPos() , self.size*0.9, True) )
        #screen.screen.blit(self.label, (self.getPos() - self.labelS/2).asTuple())
