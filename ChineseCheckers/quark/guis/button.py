import pygame
from pygame.locals import *

from Colors import *
from vec import Vec2

from component import Component

def printAction(button):
    print 'Button %s pressed!' % button.name

def rectButton(screen, button):
    x,y = button.getPos()
    w,h = button.getSize()
    rect = button.rect
    screen = screen.screen
    if button.bColor:
        pygame.draw.rect(screen, button.bColor, (x,y,w,h))
    if pygame.font:
        font = pygame.font.Font(None, int(h/2))
        text = font.render(button.name, 1, button.fColor)
        textpos = text.get_rect(centerx=x + int(w/2), centery= y + int(h/2))
        screen.blit(text, textpos)
    if button.selected:
        lines = rect.corners()
        pygame.draw.lines(screen, red, True, lines)

class Button(Component):
    def __init__(self, rect, name=''):
        Component.__init__(self, rect, name)

        self.action = printAction
        self.draw = rectButton

        self.selected = False

    def getSize(self):
        return self.rect.width, self.rect.height

    def activate(self):
        self.action(self)

    def render(self, screen):
        self.draw(screen, self)

    def EventAction(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.contains(Vec2(event.pos) - self.parent.getPos()):
                pass#self.parent.select(self)
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.contains(Vec2(event.pos) - self.parent.getPos()):
                self.activate()
                return True
        if event.type == pygame.KEYDOWN:
            if self.selected:
                if event.key == K_RETURN:
                    self.activate()
                    return True
        return False
