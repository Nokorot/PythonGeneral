from gui import *

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
        self.mainMenu = mainMenu
        self.game = game

        self.menu = None
        self.pauseMenu = PauseMenu(self)
        self.finalMenu = FinalMenu(self)

        self.serverClient = mainMenu.serverClient
        size = Vec([int(i) for i in size.strip().split(',')])

        self.gameState = ['[-]', 'Connection to the Server!']
        self.currentPlayer = -1

        self.players = [0,0]
        self.level = Level(self, size) # size
        Aplication.__init__(self)
        self.add(self.level)

        self.updateTimer = 0

    def eventHandeler(self, event):
        if self.menu != None:
            self.menu.eventHandeler(event)
            return
        Aplication.eventHandeler(self, event)
        if (event.type == pygame.KEYUP):
            if (event.key == pygame.K_p):
                self.pause();
        if (event.type == pygame.MOUSEBUTTONUP):
            loc = pygame.mouse.get_pos()

            level = self.level
            loc = Vec(loc) - level.getPos() + level.size * 0.5
            pos = int(loc[0] / level.size[0] * level.levelSize[0])

            print self.playerKey
            self.place(pos)

    def pause(self):
        # TODO: pause on "lost focus"
        self.menu = self.pauseMenu

    def openFinalMenu(self):
        #if self.gameState[0] == '[1]':
        if int(self.gameState[1]) == self.playerIndex:
            self.finalMenu.setTextDisplayed('Congratulatons \nYou have Won!')
            self.menu = self.finalMenu

    def endGame(self):
        self.serverClient.request('endGame::' + self.game)

    def place(self, pos):
        if self.currentPlayer != self.playerIndex:
            print "It is not your turn!"; return
        if self.gameState[0] != '0':
            print self.gameState
        url = '::'.join(['place', self.game, self.playerKey, str(pos)])
        responce = self.serverClient.request(url).split(':')
        resp = responce.split(':')
        if resp[0] == '[0]':
            self.level.addTile(self.playerIndex, pos)
            self.currentPlayer = (self.currentPlayer + 1) % len(self.players)
        elif resp[0] == '[1]':
            self.gameState = resp
            self.openFinalMenu()
        else:
            print responce

    def update(self):
        Aplication.update(self)
        if self.updateTimer % 120 == 0:
            # TODO: move this recpoce in to a unique sync!!

            responce = self.serverClient.request('gameState::' + self.game)
            if responce != None:
                [levelState, player, gameState] = responce.split('::')
                self.gameState = gameState

                if self.gameState[0] == '[0]': pass
                elif self.gameState[0] == '[1]':
                    self.openFinalMenu()

                self.currentPlayer = int(player)
                self.level.updateLevel(levelState)
        self.updateTimer += 1
        if self.menu != None:
            self.menu.update()

    def render(self, screen):
        Aplication.render(self, screen)
        if self.menu != None:
            self.menu.render(screen)

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

class PauseMenu(Gui):
    def __init__(self, game):
        Gui.__init__(self, game.mainMenu.bounds())
        self.mainMenu = game.mainMenu

        grid = self.getGrid([1, 2, 1], [2, 1, 1, 1, 2], 10)

        nameL = Label(grid.getRect(1, 1), 'Game Paused')
        self.addComponent(nameL)

        resumeB = Button(grid.getRect(1, 2), 'Resume')
        def resumeAction(button):
            game.menu = None
        resumeB.action = resumeAction
        self.addComponent(resumeB)

        mainMenuB = Button(grid.getRect(1, 3), 'Main Menu')
        def mainMenuAction(button):
            game.mainMenu.menu = None
            game.endGame()
        mainMenuB.action = mainMenuAction;
        self.addComponent(mainMenuB)

class FinalMenu(Gui):
    def __init__(self, game):
        Gui.__init__(self, game.mainMenu.bounds())
        self.mainMenu = game.mainMenu

        grid = self.getGrid([1, 2, 1], [2, 1, 1, 1, 2], 10)

        self.displayL = Label(grid.getRect(1, 1), 'Game Ended')
        self.addComponent(self.displayL)

        mainMenuB = Button(grid.getRect(1, 3), 'Main Menu')
        def mainMenuAction(button):
            pass
        mainMenuB.action = mainMenuAction;
        self.addComponent(mainMenuB)

    def setTextDisplayed(self, text):
        self.displayL.text = text
