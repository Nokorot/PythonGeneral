#!/usr/bin/env python

import os, sys, inspect
import pygame
from pygame.locals import *
from helpers import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

os.chdir(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
sys.path.insert(0, os.path.abspath('utils'))
sys.path.insert(0, os.path.abspath('guis'))

import options

from Colors import *
from util import *
from fpsSync import *
from game import Game, sSize
from mainMenu import MainMenu

class GameMain:

    def __init__(self, width=640,height=480):
        pygame.init()
        self.width = width - width % sSize
        self.height = height - height % sSize

        self.screen = pygame.display.set_mode((self.width, self.height), flags=pygame.RESIZABLE)

        options.load()

        self.background = black
        self.gameState = 1

        self.mainMenu = MainMenu(self)
        self.game = Game(self)

    def start(self):
        self.sync = Sync(self.update, 1/60.0)
        self.sync.sync()

    def exit(self):
        self.sync.stop()
        sys.exit()

    def update(self):
        state = self.getState()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            state.eventCathcer(event)

        state.update()

        self.screen.fill(self.background)
        state.render(self.screen)
        pygame.display.flip()

    def setState(self, state):
        self.gameState = state

    def getState(self):
        return {
            0: self.mainMenu,
            1: self.game
        }[self.gameState]


if __name__ == "__main__":
    width, height = 800, 600
    if len(sys.argv) >= 3:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
    print(width, height)
    MainWindow = GameMain(width, height)
    MainWindow.start()
