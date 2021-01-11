
import pygame
from sprite import qSprite

class qSpreteSheet():
    data = None
    sprites = None
    def __init__(self, pygame_surface):
        self.data = pygame_surface

    def __getitem__(self, key):
        if self.sprites:
            print key
            return self.sprites[key]
        else:
            return None

    def subsurface(self, x=0, y=0, width=1, height=1):
        w,h = self.data.get_size()
        return qSprite(self.data.subsurface((x*w, y*h, width*w, height*h)))

class qGridSpriteSheet(qSpreteSheet):
    X,Y = None, None
    def __init__(self, pygame_surface, X, Y):
        """
        pygame_surface: A pygame surface containging the spritesheet image,
        X: The number of columns in the sheed grid,
        Y: The number of rows in the sheed grid.
        """
        qSpreteSheet.__init__(self, pygame_surface)
        self.genSpriteGrid(X, Y)

    def genSpriteGrid(self, X, Y):
        self.X, self.Y = X, Y
        rects = [(x/float(X), y/float(Y), 1/float(X), 1/float(Y)) for y in range(Y) for x in range(X) ]
        self.sprites = [self.subsurface(*rect) for rect in rects]

class qSpriteSheetHandeler():
    spriteSheets = {}

    def loadFile(self, filename):
        if filename != None:
            return pygame.image.load(filename)
        return None

    def loadSSheetFile(self, filename):
        """ filename: .json file """
        if self.spriteSheets.__contains__(filename):
            return self.spriteSheets[filename]
        from quark.properties import sprite_sheet_folder
        data = self.loadFile(sprite_sheet_folder + filename)
        if data != None:
            pass#sheet =

    def loadGridSpriteSheet(self, filename, X, Y):
        if self.spriteSheets.__contains__((filename, X, Y)):
            return self.spriteSheets[(filename, X, Y)]
        from quark.properties import texture_folder
        data = self.loadFile(texture_folder+filename)
        if data != None:
            sheet = qGridSpriteSheet(data, X, Y)
            qSpriteSheetHandeler.spriteSheets[(filename, X, Y)] = sheet
            return sheet
        return None
