
import pygame
from Colors import *
from vec import *

class Screen():

    def __init__(self, width, height):
        self.background = red
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.center = (self.width/2, self.height/2)

    def clear(self):
        self.screen.fill(self.background)

    def rect(self, color, Rect, width=0):
        pygame.draw.rect(self.screen, color, Rect, width)

    def polygon(self, color, points, width=0):
        pygame.draw.polygon(self.screen, color, points, width)

    def circle(self, color, pos, radius, width=0):
        if isinstance(pos, Vec):
            pos = tuple(pos.floor())
        pygame.draw.circle(self.screen, color, pos, int(radius), width)

    def ellipse(self, color, Rect, width=0):
        pygame.draw.ellipse(self.screen, color, Rect, width)

    def arc(self, color, Rect, atart_angle, end_angle, width=1):
        pygame.draw.arc(self, color, Rect, atart_angle, stop_angle, width)

    def line(self, color, start_pos, end_pos, width=1):
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)

    def lines(self, color, points, closed=False, width=1):
        pygame.draw.lines(self.screen, color, closed, points, width)

    def aaline(self, color, startpos, endpos, blend=1):
        pygame.draw.aaline(self.screen, color, startpos, endpos, blend)

    def aalines(self, color, closed, pointlist, blend=1):
        pygame.draw.aalines(self.screen, color, closed, pointlist, blend)

    def blit(self, image, dest, area=None, special_flags=0):
        self.screen.blit(image, tuple(dest), area)


def makeRect(pos, size, center=False):
    if (center):
        return (pos[0] - size[0]/2, pos[1] - size[1]/2, size[0], size[1])
    return (pos[0], pos[1], size[0], size[1])
