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
        font = pygame.font.Font(None, int(rect.height/4 * textField.nameSize))
        text = font.render(textField.name, 1, textField.aColor)
        textpos = text.get_rect(x=rect.x + 5, y= rect.y + 5)
        screen.blit(text, textpos)

        font = pygame.font.Font(None, int(rect.height/2 * textField.textSize))
        t = ' ' + textField.text
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
    def __init__(self, rect, name='', text=''):
        Component.__init__(self, rect, name)
        self.text = text

        self.nameSize = 1
        self.textSize = 1

        self.legalSyms = None
        self.maxLength = 2**16

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

    def addChar(self, char):
        if self.legalSyms != None and not self.legalSyms.__contains__(char):
            return
        if self.maxLength >= 0 and len(self.text) >= self.maxLength:
            return
        self.text += char

    def EventAction(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.contains(event.pos):
                self.parent.select(self)
                return True
        if self.selected:
            if event.type == pygame.KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.addChar(event.unicode)

        return False
