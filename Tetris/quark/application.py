
import pygame, sys
from pygame.locals import *

from tick_sync import qSync
from screen import qScreen
from game_object import qGameObject
from sprites import qSpriteSheetHandeler

class qApplication(qGameObject):

    clearScreen = True
    def __init__(self, screenSize=(800, 600), **kwargs):
        pygame.init()
        self.qApp = self

        from quark.colors import qDarkGray
        self.screen = qScreen(*screenSize)
        self.screen.background = qDarkGray

        qGameObject.__init__(self, None, **kwargs)

    def qApp(self):
        return self

    def start(self):
        self.sync = qSync(self.mainLoop, 1.0/60)
        self.sync.sync()

    def stop(self):
        self.onClose()
        self.sync.stop()
        sys.exit()

    def mainLoop(self):
        self.eventHandeler()
        self.update()
        self.render()

    def eventHandeler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.stop()
            self.eventAction(event)

    def render(self):
        if self.clearScreen:
            self.screen.clear()
        qGameObject.render(self, self.screen)
        pygame.display.flip()
