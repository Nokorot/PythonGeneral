
import pygame
from helpers import load_image

def Sprite(image, x=0, y=0, width=1, height=1):
    w,h = image.get_size()
    return image.subsurface((x*w, y*h, width*w, height*h))

def SpriteShit(image, X, Y):
    return [Sprite(image, x/float(X), y/float(Y), 1/float(X), 1/float(Y)) for x in range(X) \
        for y in range(Y)]

def ShitFromFile(filename, X, Y):
    return SpriteShit(load_image(filename), X, Y)
