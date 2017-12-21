
import pygame, sys
from pygame.locals import *

from tickSync import Sync
from Colors import *
from vec import *
from screen import Screen, makeRect

class GameMain:
    def __init__(self, myApp, screenSize):
        pygame.init()

        self.screen = Screen(*screenSize)
        self.screen.background = dark_gray

        self.myApp = myApp(self)
        self.keyEventHandeler = []

        self.exit = self.stop

    def start(self):
        self.sync = Sync(self.mainLoop, 1.0/60)
        self.sync.sync()

    def stop(self):
        self.myApp.close()
        self.sync.stop()
        sys.exit()

    def mainLoop(self):
        self.eventHandeler()
        self.myApp.update()
        self.render()

    def eventHandeler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.stop()
            self.myApp.eventAction(event)

    def render(self):
        self.screen.clear()
        self.myApp.render(self.screen)
        pygame.display.flip()
