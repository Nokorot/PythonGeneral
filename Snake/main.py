#!/usr/bin/env python

import os, sys
import pygame
from pygame.locals import *
from helpers import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

sys.path.insert(0, os.path.abspath('utils'))

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

        self.screen = pygame.display.set_mode((self.width, self.height))

        options.load()

        self.background = black
        self.gameState = 0

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


import input
if __name__ == "__main__":
    MainWindow = GameMain(800, 600)
    MainWindow.start()