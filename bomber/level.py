from main import SpriteSize as SSize

from random import randint

class Level():
    def __init__(self):
        self.load()
        self.level = self.levels[0]

    def load(self, level='levels'):
        self.tiles, self.players, self.levels = LevelReader(level).load()

        for t in self.tiles:
            self.tiles[t] = Tile(self.tiles[t])

        self.ai = AI(self, self.players[1])

        self.players = [ Player(self, self.players[0], movekeys[0]) ]#[ Player(self, p, k) for p, k in zip(self.players, movekeys) ]
        self.players.append(self.ai)
        self.entities = []

    def update(self):
        for p in self.players:
            p.update()

    def render(self, screen):
        y = 0; x = 0
        for e in self.level:
            if e == ' ': y += 1; x = 0; continue
            self.tiles[e].draw(screen, x,y)
            x += 1

        for e in self.entities:
            e.render(screen);

        index = 0
        for p in self.players:
            p.render(screen, index)
            index += 1

    def getTile(self, vec):
        x, y = vec.floor()
        return self.tiles[ self.level[x + y * 12] ]

    def getTileEntity(self, vec):
        result = []
        for e in self.entities:
            if all(e.pos.floor() == vec.floor()):
                result.append(e)
        return result

    def breakTile(self, vec):
        x, y = vec.floor()

        if (self.level[x + y * 12] == '2'):
            if (randint(0, 100) > 50):
                o = NewBombObject(Vec2(x, y), self)
                self.entities.append(o)

        self.level[x + y * 12] = '1'

class Entity():
    def __init__(self, pos, level):
        self.level = level
        self.pos = pos
        self.solid = False
        self.colletable = False

class NewBombObject(Entity):
    def __init__(self, pos, level):
        Entity.__init__(self, pos, level)
        self.sprite = SpriteFromFile('blast.png')
        self.sprite.transform(size=Vec2(SSize))
        self.colletable = True

    def collect(self, player):
        player.maxbombs += 1;
        self.level.entities.remove(self)

    def render(self, screen):
        p = (self.pos + .5) * SSize
        self.sprite.draw(screen, p.floor(), center=True)
        # screen.circle((255, 0, 0), p.floor(), int(.4 * SSize))

class Tile():
    def __init__(self, info):
        info = info.split(',')
        self.name = info[0]
        self.sprite = SpriteFromFile(info[0] + '.png')
        self.sprite.transform(size=Vec2(ssize))

        self.solid = True
        self.breakable = True
        for i in info[1:]:
            value = True
            if i.startswith('!'):
                value = False; i = i[1:]
            if i == 'solid': self.solid = value
            if i == 'breakable': self.breakable = value

    def break_(self, x, y):
        return None

    def draw(self, screen, x, y):
        self.sprite.draw(screen, Vec2(x,y)*ssize, center=False)

from fileReader import LineReader
class LevelReader(LineReader):
    def __init__(self, infile):
        LineReader.__init__(self, 'data/' + infile + ".lv")

    def read(self):
        materials = {}; players = []; levels = []

        while self.next():
            self.line

            if self.line.startswith('Load'):
                while self.next() and not self.empty():
                    A = self.line.split(':')
                    materials[A[0]] = A[1].replace(' ', '')
            if self.line.startswith('Players'):
                while self.next() and not self.empty():
                    players.append(self.line.split(' '))
            if self.line.startswith('Level'):
                level = []
                while self.next() and not self.empty():
                    level += self.line.split(' ') + [' ']
                levels.append(level)

        return materials, players, levels

from sprite import SpriteFromFile, ShitFromFile
from vec import *
from main import *
from game import movekeys, Player, AI

ssize = SpriteSize
