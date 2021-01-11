
import numpy as np
from quark.maths import qVec2
from quark import qGameObject

class qTile(qGameObject):
    cord = qVec2(0,0)
    tileSize = qVec2(48, 48)

    def pos(self):
        return qVec2(self.cords) * self.tileSize

    def getPos(self):
        if self.parent == None:
            return self.pos()
        return self.pos() + self.parent.getPos();

class qTileLayer(qGameObject):
    tiles = []
    width, height = 0,0
    layerDepth = None

    def __init__(self, parent):#, width, heigt, tiles):
        qGameObject.__init__(self, parent)
        pass#self.width, self.height, self.tiles = width, height, tiles

    def add(self, instent, cords, **kwargs):
        qGameObject.add(self, instent, cords=cords, **kwargs)

class qTileLevel(qGameObject):
    size = qVec2(0,0)

    def __init__(self, tileSize, size):
        self.tileLayers = {}
        self.tileSize = tileSize
        self.size = qVec2(size) * tileSize

    def add(self, child, depth=0, **kwargs):
        if isinstance(child, qTileLayer):
            if self.tileLayers.__contains__(depth) \
                and self.tileLayers[depth] != None:
                self.tileLayers[depth].removeMe()
            self.tileLayers[depth] = child
            child.layerDepth = depth
        qGameObject.add(self, child, depth, **kwargs)
