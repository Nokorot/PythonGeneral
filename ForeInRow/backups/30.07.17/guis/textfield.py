import pygame
from pygame.locals import *

import os, sys
sys.path.insert(0, os.path.abspath('../utils'))
from Colors import *

from component import Component

def printAction(textField):
    print 'TextField %s runs action!' % textField.name

def rectField(screen, textField):
    rect = textField.rect
    if textField.bColor:
        pygame.draw.rect(screen, textField.bColor, rect.pgRect())
    if pygame.font:
        font = pygame.font.Font(None, int(rect.height/2))
        t = ' ' + textField.name
        if textField.mark:
            t += '|'
        else:
            t += ' '
        text = font.render(t, 1, textField.fColor)
        textpos = text.get_rect(centerx=rect.x + int(rect.width/2), centery= rect.y + int(rect.height/2))
        screen.blit(text, textpos)
    if textField.selected:
        lines = rect.corners()
        pygame.draw.lines(screen, red, True, lines)

class TextField(Component):
    def __init__(self, rect, name=''):
        Component.__init__(self, rect, name)

        self.action = printAction
        self.draw = rectField

        self.selected = False

        self.time = 0
        self.mark = True
        self.shift = False

    def activate(self):
        self.action(self)

    def check(self, point):
        if self.rect.contains(point):
            self.activate()
            return True
        return False

    def update(self):
        self.time = (self.time + 1) % 90
        self.mark = self.selected and self.time > 60

    def render(self, screen):
        self.draw(screen.screen, self)

    def eventHandeler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.contains(event.pos):
                self.parent.select(self)
                return True
        if self.selected:
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if 'abcdefghijklmnopqrstuvwxyz1234567890,.-'.__contains__(key):
                    if self.shift:
                        self.name += key.upper()
                    else:
                        self.name += key
                    return True
                if event.key == K_SPACE:
                    self.name += ' '
                if event.key == K_BACKSPACE:
                    self.name = self.name[:-1]
                    return True
                if [K_LSHIFT, K_RSHIFT].__contains__(event.key):
                    self.shift = True
            if event.type == pygame.KEYUP:
                if [K_LSHIFT, K_RSHIFT].__contains__(event.key):
                    self.shift = False
        return False
