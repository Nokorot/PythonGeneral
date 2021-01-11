
import pygame
from quark.maths import qVec

class qSprite():
    def __init__(self, pygame_surface):
        self.data = pygame_surface
        self.size = qVec(self.data.get_size())
        self.width = self.data.get_width()
        self.height = self.data.get_height()

    def render(self, screen, pos):
        pos = [pos[0] - self.width / 2, pos[1] - self.height / 2]
        screen.blit(self.data, pos)

    '''
    def transform(self, matrix):
        pass
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
        return Sprite(image)'''

    def scale(self, width, height, copy = False, fitScale=False):
        if width == None:
            width = height * self.width / self.height
        elif height == None:
            height = width * self.height / self.width
        elif fitScale:
            if (self.width / self.height) > (width / height):
                return self.scale(None, height, copy)
            return self.scale(width, None, copy)

        image = pygame.transform.scale(self.data, (width, height))
        if copy == False:
            self.data = image
            self.width, self.height = width, height
        return Sprite(image)

    def rotate(self, angle, copy=False):
        image = pygame.transform.rotate(self.data, angle * 180 / pi)
        if copy == False:
            self.data = image
            self.width, self.height = image.get_width(), image.get_height()
        return Sprite(image)

    def replace(self, colorA, colorB, copy=False):
        if not copy:
            px = pygame.PixelArray(self.data)
            px.replace(colorA, colorB)
            image = px.make_surface()
        else:
            px = pygame.PixelArray(self.data.copy())
            px.replace(colorA, colorB)
            image = px.make_surface()
        return Sprite(image)

class qAnimatedSprite(object):
    def __init__(self, sprites, indecies=None, fps=5):
        """
        sprites: list of sprites frames,
        fps: Nummber frames per second.
        """
        self.sprites = sprites
        self.indecies = indecies
        self.currentSprite = 0;
        self.width = sprites[0].width
        self.width = sprites[0].height
        self.time = 0
        self.fps = fps

    def update(self, dt):
        self.time += dt
        if self.time >= 1./self.fps:
            self.time -= 1./self.fps
            self.nextFrame()

    def nextFrame(self):
        if self.indecies:
            self.currentSprite = (self.currentSprite + 1) % len(self.indecies)
        else:
            self.currentSprite = (self.currentSprite + 1) % len(self.sprites)

    def render(self, screen, pos):
        if self.indecies:
            self.sprites[self.indecies[self.currentSprite]].render(screen, pos)
        else:
            self.sprites[self.currentSprite].render(screen, pos)

    def scale(self, width, height, copy=False):
        sprites = [sprite.scale(width, height, copy) for sprite in self.sprites]
        if copy: return AnimatedSprite(sprites, tpf)
        return self

    def rotate(self, angle, copy=False):
        sprites = [sprite.rotate(anlge, copy) for sprite in self.sprites]
        if copy: return AnimatedSprite(sprites, tpf)
        return self

    def replace(self, colorA, colorB, copy=False):
        sprites = [sprite.replace(colorA, colorB, copy) for sprite in self.sprites]
        if copy: return AnimatedSprite(sprites, tpf)
        return self

'''
def loadAnimatedSprite(filename, X, Y, subsection = None):
    if filename != None and type(filename) == str:
        data = pygame.image.load("res/" + filename)
        if data != None:
            if subsection == None:
                subsection = slice(0, 9223372036854775807)
            return AnimatedSprite(SpriteSheet(data, X, Y).sprites[subsection])
    return None

def loadSpriteSheet(filename, X, Y):
    if filename != None and type(filename) == str:
        data = pygame.image.load("res/" + filename)
        if data != None:
            return SpriteSheet(data, X, Y)
    return None

def loadSprite(filename):
    if filename != None and type(filename) == str:
        data = pygame.image.load("res/" + filename)
        if data != None:
            return Sprite(data)
    return None
'''
