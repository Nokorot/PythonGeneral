
import os, sys
sys.path.insert(0, os.path.abspath('site-packages'))

import pygame
from pygame.locals import *

sys.path.insert(0, os.path.abspath('utils'))
sys.path.insert(0, os.path.abspath('guis'))

from tickSync import Sync
from Colors import *
from vec import *

ScreenWidth = 800
ScreenHeight = 600
ScreenSize = Vec(ScreenWidth, ScreenHeight)

class Main():
    def __init__(self):
        pygame.init()

        import screen
        self.screen = screen.Screen(ScreenWidth, ScreenHeight)
        self.screen.background = dark_gray

        from menu_main import MainMenu
        self.mainMenu = MainMenu(self)

        #self.game = game.Game()
        self.keyEventHandeler = []

    def eventHandeler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            self.mainMenu.eventHandeler(event)

    def update(self):
        self.mainMenu.update()

    def render(self):
        self.screen.clear()
        self.mainMenu.render(self.screen)
        pygame.display.flip()

    def mainLoop(self):
        self.eventHandeler()
        self.update()
        self.render()

    def start(self):
        self.sync = Sync(self.mainLoop, 1.0/60)
        self.sync.start()

    def exit(self):
        self.sync.stop()
        sys.exit()

if __name__ == '__main__':
    main = Main()
    main.start()
