
class Game():
    def __init__(self):
        self.level = Level()
        self.gui = Gui(self.level.players)

    def update(self):
        self.level.update()

    def render(self, screen):
        self.level.render(screen)
        self.gui.render(screen)

class Player():
    def __init__(self, level, info, keys):
        self.level = level
        self.sprite = SpriteFromFile(info[0] + '.png')
        self.sprite.transform(size=Vec2(ssize)*.9)
        self.pos = Vec2(info[1:3]) + .5
        self.keys = keys
        self.speed = 5 * 1/60.
        self.cooldown = 0
        self.firerate = 2 # per secound

        self.colition = [-.4, .4, -.4, .4]

        self.name = info[0]
        self.lifes = 3
        self.dead = False

        self.maxbombs = 1
        self.bombs = []

    def update(self):
        if self.dead: return
        keys = pygame.key.get_pressed()
        u = keys[self.keys['up']]
        d = keys[self.keys['down']]
        r = keys[self.keys['right']]
        l = keys[self.keys['left']]
        self.move(r-l, d-u)

        [b.update() for b in self.bombs]
        self.cooldown -= 1
        if keys[self.keys['bomb']] and self.cooldown <= 0:
            if len(self.level.getTileEntity(self.pos)) <= 0:
                if len(self.bombs) < self.maxbombs:
                    self.bombs.append( Bomb(self.pos, self) )
                    self.cooldown = 60 / self.firerate

    def move(self, x, y):
        if x == 0 and y == 0: return
        xdes = Vec2(self.pos)
        ydes = Vec2(self.pos)
        xdes[0] += x * self.speed
        ydes[1] += y * self.speed

        if not self.colides(self.pos, xdes):
            self.pos[0] = xdes[0]
        if not self.colides(self.pos, ydes):
            self.pos[1] = ydes[1]

        for e in self.level.getTileEntity(self.pos):
            if (e.colletable):
                e.collect(self)

    def colides(self, current, dest):
        for i in range(4):
            x = self.colition[i % 2]
            y = self.colition[i / 2 + 1]
            if IVec(dest + Vec2(x, y)) == IVec(current + Vec2(x,y)):
                continue
            if self.level.getTile(dest + Vec2(x, y)).solid:
                return True
            for e in self.level.getTileEntity(dest + Vec2(x, y)):
                if e.solid:
                    return True
        return False

    def render(self, screen, index):
        if self.dead: return
        [b.render(screen) for b in self.bombs]

        self.sprite.draw(screen, (self.pos) * ssize)

    def loseLife(self):
        self.lifes -= 1
        self.dead = self.lifes <= 0

import random

class AI(Player):
    def __init__(self, level, info):
        Player.__init__(self, level, info, None)
        self.dir = 0

    def update(self):
        num = random.randint(0, 30)
        if (num > 21):
            self.dir = num - 21

        #self.dir = 4
        self.move(self.dir % 3 - 1, self.dir / 3 - 1)



class Gui():
    def __init__(self, players):
        self.players = players
        self.sprites = ShitFromFile("gui.png", 1, 1)
        self.heart = self.sprites[0]

        self.size = Vec(3, 1) * ssize
        self.heartw = self.size[1] / 2
        self.heart.transform(size=Vec2(self.heartw))

        self.offsets = np.array([Vec(x,y) for y in range(2) for x in range(2)])
        self.offsets *= (ScreenPSize - self.size)

    def render(self, screen):
        index = 2
        for p in self.players:
            offset = self.offsets[index]
            for i in range(p.lifes):
                x = (.5 + i) * self.heartw * 1.1
                y = self.size[1] * 3 / 4
                self.sprites[0].draw(screen, Vec(x,y) + offset)
            index += 1

from vec import *
from Colors import *

from main import *
ssize = SpriteSize

p1 = { # Player 1
    'bomb': pygame.K_RETURN,     \
    'up': pygame.K_UP,         \
    'down': pygame.K_DOWN,     \
    'right': pygame.K_RIGHT,   \
    'left': pygame.K_LEFT     }
p2 = { # Player 2
    'bomb': pygame.K_e,        \
    'up': pygame.K_w,          \
    'down': pygame.K_s,        \
    'right': pygame.K_d,       \
    'left': pygame.K_a        }
movekeys = [p1, p2]


from sprite import SpriteFromFile, ShitFromFile
from level import Level, Entity

class Bomb(Entity):
    def __init__(self, pos, parent):
        Entity.__init__(self, IVec(pos), parent.level)
        self.parent = parent
        self.lifetime = 2 * 60
        self.firetime = 1 * 60
        self.firing = False
        self.solid = True

        self.players = self.level.players[:]

        self.sprite = SpriteFromFile('bomb' + '.png')
        self.sprite.transform(size=Vec2(ssize))
        self.blastsprite = SpriteFromFile('blast' + '.png')
        self.blastsprite.transform(size=Vec2(ssize))

        self.sheet = ShitFromFile('bomb2.png', 2, 2)
        [s.transform(size=Vec2(ssize)) for s in self.sheet]
        self.sprite = self.sheet[0]

        self.level.entities.append(self)

    def update(self):
        self.lifetime -= 1
        if self.lifetime == 0:
            self.fire()
        if self.lifetime < -self.firetime:
            self.parent.bombs.remove( self )
            self.level.entities.remove( self )
            del self; return

        if self.firing:
            i = len(self.players)
            while i > 0:
                i -= 1
                p = self.players[i]
                if self.blast.__contains__(IVec(p.pos) - self.pos):
                    p.loseLife()
                    self.players.pop(i)


    def fire(self):
        self.firing = True
        bx, by = self.pos.asTuple()

        self.blast = []
        def apply(x, y):
            tile = self.level.getTile(Vec(bx+x, by+y))
            if tile.breakable:
                self.blast.append(Vec(x,y))
                self.level.breakTile(Vec(bx+x, by+y))
            return tile.solid

        f = 0xf
        apply(0, 0)
        for i in range(1,3):
            if f & 1 and apply( i, 0): f &= 14 #0xe
            if f & 2 and apply(-i, 0): f &= 13 #0xd
            if f & 4 and apply( 0, i): f &= 11 #0xb
            if f & 8 and apply( 0,-i): f &= 7  #0x7

    def render(self, screen):
        if not self.firing:
            self.sprite.draw(screen, (self.pos + .5) * ssize)
        else:
            for b in self.blast:
                i = 1 if b[0] else 2 if b[1] else 3
                self.sheet[i].draw(screen, (self.pos + b + .5) * ssize)
