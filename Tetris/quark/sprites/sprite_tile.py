
from random import randint
from sprite_sheet import qSpriteSheetHandeler
from sprite import qAnimatedSprite
from quark.tile_grid import qLevelDataObject, qTile, qTileLevelFileReader
from quark.maths import qVec2

from quark.sprites import spriteSheetHandeler as ssHandeler

class qSimpleSpriteTile(qTile):
    def __init__(self, sprite):
        self.sprite = sprite

    def Render(self, screen):
        pos = self.getPos()
        if self.sprite:
            self.sprite.render(screen, self.getPos())

class qAnimatedSpriteTile(qSimpleSpriteTile):
    def Update(self):
        self.sprite.update()

class SpriteSheetData(qLevelDataObject):
    def __init__(self, reader, data):
        qLevelDataObject.__init__(self, reader, data)
        filename = data["file"]
        self.sheet = ssHandeler.loadSpriteSheet(filename)
        self.symbols = {k:(v[0] + v[1]*XY[0]) for (k,v) in zip(data['symbols'], data['values'])}
        self.tiles = {}

    def getSymbolData(self, symbol):
        if self.tiles.__contains__(symbol):
            return self.tiles[symbol]
        sprite = self.sheet[self.symbols[symbol]]
        if isinstance(sprite, qAnimatedSprite):
            tile = qAnimatedSpriteTile(sprite)
        else: tile = qSimpleSpriteTile(sprite)
        self.tiles[symbol] = tile
        return tile
#qTileLevelFileReader.levelDataObjects['SpriteSheets'] = SpriteSheetData

class GridSpriteSheetData(qLevelDataObject):
    def __init__(self, reader, data):
        qLevelDataObject.__init__(self, reader, data)
        filename, XY = data['file'], data['XY']
        self.sheet = ssHandeler.loadGridSpriteSheet(filename, *XY)
        self.symbols = {k:(v[0] + v[1]*XY[0]) for (k,v) in \
                    zip(data['symbols'], data['values'])}
        self.tiles = {}

    def getSymbolData(self, symbol):
        if self.tiles.__contains__(symbol):
            return self.tiles[symbol]
        tile = qSimpleSpriteTile(self.sheet[self.symbols[symbol]])
        self.tiles[symbol] = tile
        return tile
qTileLevelFileReader.levelDataObjects['GridSpriteSheets'] = GridSpriteSheetData
