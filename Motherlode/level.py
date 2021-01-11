
from vec import *
from entity import *

import random

BlockSize = IVec(50, 50)
ChunkSize = IVec(10, 10)
CPS = ChunkSize * BlockSize # ChunkPixelSize

counter = 0

class Block():
    def __init__(self, level, cords, blockType):
        self.cords = cords
        self.type = blockType
        self.pos = self.cords*BlockSize
        self.level = level

        self.color = random.randint(0, 256*256*256)

    def Render(self, screen, pos):
        x, y = pos
        w, h = BlockSize
        screen.rect((self.color >> 16, (self.color >> 8) & 255, (self.color) & 255), (x, y, w, h))

class Chunk():

    def __init__(self, level, cords):
        self.pos = cords * CPS
        self.cords = cords
        self.level = level

        self.generate()

    def newBlock(self, x,y):
        return Block(self.level, Vec(x,y) + self.cords * ChunkSize, 0)

    def generate(self):
        self.bloks = []
        for y in range(ChunkSize[1]):
            for x in range(ChunkSize[0]):
                self.bloks.append(self.newBlock(x, y))

    def Render(self, screen):
        for j in range(ChunkSize[1]):
            y = (j + self.cords[1] * ChunkSize[1]) * BlockSize[1] + screen.center[1] - self.level.camera[1]
            if (y < -BlockSize[1] or y > screen.height): continue
            for i in range(ChunkSize[0]):
                x = (i + self.cords[0] * ChunkSize[0]) * BlockSize[0] + screen.center[0] - self.level.camera[0]
                if (x < -BlockSize[0] or x > screen.width): continue
                self.bloks[i + j * ChunkSize[0]].Render(screen, (x, y))

class Level(Entity):
    def __init__(self, camera):
        Entity.__init__(self, (0,0))
        self.chunks = []
        self.camera = camera

    def generate(self, chunks):
        chunks = chunks[:]
        
        for chunk in self.chunks:
            if (chunks.__contains__(chunk.cords)):
                chunks.remove(chunk.cords)

        for chunk in chunks:
            self.chunks.append(Chunk(self, chunk))

    def Render(self, screen, pos):
        pos = self.camera
        size = (screen.width, screen.height)

        chunks = getChunksInside(pos, size)
        self.generate(chunks)

        for chunk in self.chunks:
            if (chunks.__contains__(chunk.cords)):
                chunk.Render(screen)


def getChunksInside(pos, size):
    def round(p):
        x = int(p[0]) if p[0]>0 else int(p[0])-1
        y = int(p[1]) if p[1]>0 else int(p[1])-1
        return IVec(x,y)

    corners = [ Vec( (pos[0] - size[0] / 2), (pos[1] - size[1] / 2) ),
                Vec( (pos[0] + size[0] / 2), (pos[1] + size[1] / 2) )]
    corners = [ round(p / CPS) for p in corners ]

    chunks = []
    for j in range(corners[0][1], corners[1][1]+1):
        for i in range(corners[0][0], corners[1][0]+1):
            chunks.append(Vec(i,j))
    return chunks;
