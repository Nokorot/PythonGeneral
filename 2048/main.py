#!/usr/bin/python

import os, sys
import pygame
from pygame.locals import *

sys.path.insert(0, os.path.abspath('utils'))

from tickSync import Sync
from Colors import *
from vec import *

import game
import screen
from screen import makeRect

ScreenWidth = 800;
ScreenHeight = 600;
ScreenSize = Vec(ScreenWidth, ScreenHeight)

class GameMain:
    def __init__(self):
        pygame.init()

        self.screen = screen.Screen(ScreenWidth, ScreenHeight)
        self.screen.background = dark_gray
        self.game = game.Game()
        self.keyEventHandeler = []

    def start(self):
        self.sync = Sync(self.mainLoop, 1.0/60)
        self.sync.sync()

    def stop(self):
        self.sync.stop()
        sys.exit()

    def mainLoop(self):
        self.eventHandeler()
        self.update()
        self.render()

    def eventHandeler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.stop()
            self.game.eventAction(event)

    def update(self):
        self.game.update()

    def render(self):
        self.screen.clear()
        self.game.render(self.screen)
        pygame.display.flip()


from entity import *
from vec import *

if __name__ == '__main__':
    main = GameMain()
    main.start()
