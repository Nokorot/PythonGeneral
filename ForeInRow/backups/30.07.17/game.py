
from entity import *
from vec import *
from Colors import *
from sprite import SpriteFromFile, ShitFromFile

import random

from main import *

def MakeFiRGame(mainMenu, game, size):
    serverClient = mainMenu.serverClient
    ppk = serverClient.rsa_public_key
    s_url = 'make::' + game + '::' + ppk + '::' + size
    responce = serverClient.request(s_url)
    [key,info] = responce.split('::')

    game = FiRGame(mainMenu, game, size)
    game.playerKey = serverClient.decrypt(key)
    game.playerIndex = 0 # int(info[*])

    return game

def ConnectFiRGame(mainMenu, game):
    serverClient = mainMenu.serverClient
    ppk = serverClient.rsa_public_key

    s_url = '::'.join(['connect', game, ppk])
    responce = serverClient.request(s_url)
    [key,size] = responce.split('::')

    game = FiRGame(mainMenu, game, size)
    game.playerKey = serverClient.decrypt(key)
    game.playerIndex = 1 # int(info[*])

    return game

class FiRGame(Aplication):

    def __init__(self, mainMenu, game, size):
        self.serverClient = mainMenu.serverClient
        self.game = game
        size = Vec([int(i) for i in size.strip().split(',')])

        self.currentPlayer = -1

        self.players = [0,0]
        self.level = Level(self, size) # size
        Aplication.__init__(self)
        self.add(self.level)

        self.updateTimer = 0

    def eventHandeler(self, event):
        if (event.type == pygame.MOUSEBUTTONUP):
            loc = pygame.mouse.get_pos()

            level = self.level
            loc = Vec(loc) - level.getPos() + level.size * 0.5
            pos = int(loc[0] / level.size[0] * level.levelSize[0])

            print self.playerKey
            self.place(pos)

    def place(self, pos):
        if self.currentPlayer != self.playerIndex:
            print "It is not your turn!"; return
        url = '::'.join(['place', self.game, self.playerKey, str(pos)])
        responce = self.serverClient.request(url)
        if responce.split(':')[0] == '[0]':
            self.level.addTile(self.playerIndex, pos)
            self.currentPlayer = (self.currentPlayer + 1) % len(self.players)
        else:
            print responce

    def Update(self):
        self.updateTimer += 1
        if self.updateTimer % 120 == 0:
            gameState = self.serverClient.request('gameState::' + self.game)
            [levelState, player] = gameState.split('::')

            self.currentPlayer = int(player)
            self.level.updateLevel(levelState)

class Level(Entity):

    def __init__(self, game, size):
        Entity.__init__(self,  ScreenSize / 2)
        self.game = game

        frac = ScreenSize / size
        self.tileSize = int( min(frac[0], frac[1]) * 0.9)
        self.size = size * self.tileSize

        self.levelSize = IVec(size[0], size[1])


        self.tiles = [None for _ in range(self.levelSize[0] * self.levelSize[1])]
        self.grid = [(Vec(x, y) + 0.5) * self.tileSize - self.size * 0.5 \
                                    for y in range(self.levelSize[1]) \
                                    for x in range(self.levelSize[0])]

        self.levelState = '-' * int(size[0] * size[1])

    def getTile(self, x, y):
        return self.tiles[x + y * self.levelSize[0]]

    def addTile(self, player, pos=0, loc=None):
        for i in range(self.levelSize[1]):
            if (self.getTile(pos, i) != None):
                if (i == 0): return False
                i -= 1; break

        i = pos + i * self.levelSize[0]

        l = list(self.levelState)
        l[i] = str(player)
        self.levelState = ''.join(l)

        self.tiles[i] = Tile(self, (self.grid[pos], self.grid[i]), player)

    def updateLevel(self, levelState):
        if (levelState != self.levelState):
            i = 0
            for a,b in zip(levelState, self.levelState.strip()):
                if a != b:
                    self.addTile(int(a), i % self.levelSize[0])
                i += 1

    def Render(self, screen, pos):
        for loc in self.grid:
            screen.circle(light_gray, tuple((loc + self.getPos()).floor()), int(self.tileSize * 0.48))

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

            if (abs(delta.norm()) > self.moveSpeed):
                self.pos = self.pos + delta.normalize() * self.moveSpeed;
            else:
                self.pos = self.newPos

    def Render(self, screen, pos):
        from math import log

        screen.circle(self.Colors[self.color], self.getPos().floor(), self.size / 2)

        #screen.rect( self.Colors[int(log(self.value) / log(2)) - 1], #makeRect(self.getPos() , self.size*0.9, True) )
        #screen.screen.blit(self.label, (self.getPos() - self.labelS/2).asTuple())
