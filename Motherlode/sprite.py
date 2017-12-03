
from vec import *

import pygame
from helpers import load_image

def has(a, b):
    return a.__contains__(b)

class Sprite():
    def __init__(self, image):
        self.size = Vec(image.get_size())
        self.image = image

    def transform(self, keep=True, **kws):
        image = self.image
        for kw in kws:
            value = kws[kw]
            if kw=='size':
                if not isinstance(value, Vec): value = Vec(value)
                image = pygame.transform.scale(image, value.floor())
                self.size.set(value)
            if kw=='rotate':
                image =pygame.transform.rotate(image, value.floor())
        if keep:
            self.image = image
        return image

    def draw(self, screen, pos, center=True, **kws):
        if not isinstance(pos, Vec): pos = Vec(pos)

        if center: pos = pos - self.size / 2

        screen.blit( self.transform(False, **kws) , pos)


def subsprite(image, x=0, y=0, width=1, height=1):
    w,h = image.get_size()
    return Sprite(image.subsurface((x*w, y*h, width*w, height*h)))

def SpriteShit(image, X, Y):
    return [subsprite(image, x/float(X), y/float(Y), 1/float(X), 1/float(Y)) for x in range(X) \
        for y in range(Y)]

def SpriteFromFile(filename):
    return Sprite(load_image(filename, (255, 0, 255)))

def ShitFromFile(filename, X, Y):
    return SpriteShit(load_image(filename, (255, 0, 255)), X, Y)
