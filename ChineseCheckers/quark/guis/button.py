import pygame
from pygame.locals import *

from Colors import *

from component import Component

def printAction(button):
    print 'Button %s pressed!' % button.name

def rectButton(screen, button):
    rect = button.rect
    screen = screen.screen
    if button.bColor:
        pygame.draw.rect(screen, button.bColor, rect.pgRect())
    if pygame.font:
        font = pygame.font.Font(None, int(rect.height/2))
        text = font.render(button.name, 1, button.fColor)
        textpos = text.get_rect(centerx=rect.x + int(rect.width/2), centery= rect.y + int(rect.height/2))
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

    def activate(self):
        self.action(self)

    def render(self, screen):
        self.draw(screen, self)

    def EventAction(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.contains(event.pos):
                pass#self.parent.select(self)
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.contains(event.pos):
                self.activate()
                return True
        if event.type == pygame.KEYDOWN:
            if self.selected:
                if event.key == K_RETURN:
                    self.activate()
                    return True
        return False
