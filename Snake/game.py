import pygame
from pygame.locals import *

import options

from random import randint
from Colors import *
from util import *
from gui import *

sSize = 32

# Arrow keys
# Left = pygame.K_LEFT #pygame.K_h
# Right = pygame.K_RIGHT #l
# Up = pygame.K_UP #k
# Down = pygame.K_DOWN #j

# Vim keys
Left = pygame.K_h
Right = pygame.K_l
Up = pygame.K_k
Down = pygame.K_j

class Game():
    def __init__(self, main):
        self.main = main
        self.w = main.width // sSize
        self.h = main.height // sSize

        self.bgSprite = pygame.transform.scale(load_image('bg 4.jpg'), (main.width, main.height))

        self.restartMenu = RestatMenu(self, (main.width, main.height))
        self.pauseMenu = PauseMenu(self, (main.width, main.height))

        self.reset()

    def reset(self):
        w, h = self.w, self.h
        self.snake = Snake(w,h, (w//2, h//2))
        self.pellet = Pellet(w, h)
        self.isDead = False
        self.paused = False

    def update(self):
        if self.isDead:
            self.restartMenu.update()
            return
        if self.paused:
            self.pauseMenu.update()
            return
        self.snake.move()
        """Check for pellet"""
        p = self.snake.getPos()
        if (p == self.pellet.pos):
            self.snake.eat()
            self.pellet.move(self.snake.getPositions())
        """Check for deth"""
        if (self.snake.getPositions()[0:-1].__contains__(p)):
            print('dead')
            self.isDead = 1
            return

    def render(self, screen):
        screen.blit(self.bgSprite, (0,0))
        self.drawGame(screen)
        self.drawPauseinfo(screen)
        if self.paused:
            self.pauseMenu.render(screen)
        if self.isDead:
            self.restartMenu.render(screen)

    def eventCathcer(self, event):
        if self.paused:
            self.pauseMenu.eventCathcer(event)
        if event.type == KEYDOWN:
            if self.isDead:
                self.restartMenu.eventCathcer(event)
                return
            if (event.key == K_p):
                self.paused = not self.paused
            if self.paused: return

            if {Right, Left, Up, Down}.__contains__(event.key):
                self.snake.turn(event.key)

    def drawGame(self, screen):
        self.pellet.draw(screen)
        self.snake.draw(screen)
        self.drawScore(screen)

    def drawScore(self, screen):
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("Pellets %s" % self.snake.pellets, 1, white)
            textpos = text.get_rect(centerx=self.w * sSize/2)
            screen.blit(text, textpos)

    def drawPauseinfo(self, screen):
        font = pygame.font.Font(None, 20)
        text = font.render("Press p to pause", 1, white)
        textpos = text.get_rect(x=sSize)
        screen.blit(text, textpos)

    def pause(self, b):
        self.paused = b

import helpers
from sprite import *
class Snake():
    def __init__(self, w, h, pos=(2,2), direct=0):
        self.w = w
        self.h = h
        self.parts=[[pos, direct, 0]]

        self.direct = 0

        self.grow = 2
        self.pellets = 0
        self.sleep = 10-options.dificolty*1.5
        self.count = 200
        self.x, self.y = 0, 0

        from random import randint
        options.setColor((randint(0,255),randint(0,255),randint(0,255)))
        self.head = options.snake[0]
        self.tail = options.snake[1]
        self.strait = options.snake[2]
        self.turnS = options.snake[3]

        def scale(img):
            return pygame.transform.scale(img, (sSize, sSize))
        [self.head, self.tail, self.strait, self.turnS] = map(scale, [self.head, self.tail, self.strait, self.turnS])

    def getPos(self, i=0):
        return self.parts[-1-i][0]

    def getPositions(self):
        return [self.parts[i][0] for i in range(len(self.parts)) ]

    def draw(self, screen):
        s2 = sSize / 2
        i = 0
        for part in self.parts:
            if i == len(self.parts) -1:
                dr = part[1]
                if dr % 2 == 1:
                    im = pygame.transform.rotate( self.head, 90 * dr )
                else:
                    im = pygame.transform.flip( self.head, dr == 2, False )
            elif i == 0:
                dr = self.parts[i+1][1]
                im = pygame.transform.rotate(self.tail, 90 * dr)
            else:
                dr =  part[1]
                if part[2] == 0:
                    im = pygame.transform.rotate(self.strait, 90 * dr)
                else:
                    im = pygame.transform.flip( self.turnS, False, dr  == (self.parts[i+1][1] + 1) % 4)
                    im = pygame.transform.rotate( im, 90 * dr )
            screen.blit(im, scale2(part[0], sSize))
            i=i+1

    def turn(self, key):
        nd = {
            Right: 0,
            Up:    1,
            Left:  2,
            Down:  3
        }[key]
        if not ((nd + self.direct) % 2 == 0 or nd == self.direct):
            self.direct = nd
            self.count = self.sleep
            self.parts[-1][2] = 1
            self.move()

    def move(self):
        self.count += 1
        if(self.count > self.sleep):
            x = self.getPos()[0] - ((self.direct + 1) % 2) * sgn(self.direct - 1)
            y = self.getPos()[1] + ((self.direct) % 2) * sgn(self.direct - 2)
            self.parts.append([(x % self.w, y % self.h), self.direct, 0])

            if self.grow > 0:
                self.grow -= 1
            else:
                self.parts.pop(0)
            self.count = 0

    def eat(self):
        self.grow += 1
        self.pellets += 1

class Pellet():
    def __init__(self, w,h):
        self.w = w
        self.h = h
        self.color = red
        self.move()

    def draw(self, screen):
        s2 = sSize / 2
        pygame.draw.circle(screen, self.color, add2(scale2(self.pos, sSize), (int(s2), int(s2))), int(s2))

    def move(self, ipos=[]):
        p = []
        for y in range(int(self.h-1)):
            for x in range(int(self.w-1)):
                if not ipos.__contains__((x,y)):
                    p.append((x,y))
        self.pos = p[randint(0, len(p) -1)]

class PauseMenu(Gui):
    def __init__(self, game, bounds):
        Gui.__init__(self, bounds)

        grid = Gui.getGrid(self, [1,2,1], 5, 10)

        resumeB = Button(grid.getRect(1, 1), 'Resume')
        resumeB.action = lambda button: (game.pause(False))
        resumeB.bColor = None
        Gui.addComponent(self, resumeB)

        restartB = Button(grid.getRect(1, 2), 'Restart')
        restartB.action = lambda button: (game.reset())
        restartB.bColor = None
        Gui.addComponent(self, restartB)

        '''mainB = Button(grid.getRect(1, 3), 'Main Menu')
        mainB.action = lambda button: (game.reset(), game.main.setState(0))
        mainB.bColor = None
        Gui.addComponent(self, mainB)'''

        mainB = Button(grid.getRect(1, 3), 'Quite')
        mainB.action = lambda button: (game.main.exit())
        mainB.bColor = None
        Gui.addComponent(self, mainB)

    def render(self, screen):
        Gui.render(self, screen)

class RestatMenu(Gui):
    def __init__(self, game, bounds):
        Gui.__init__(self, bounds)

        grid = Gui.getGrid(self, [1,2,1], 4, 10)

        restartB = Button(grid.getRect(1, 1), 'Restart')
        restartB.action = lambda button: (game.reset())
        restartB.bColor = None
        Gui.addComponent(self, restartB)

        '''mainB = Button(grid.getRect(1, 2), 'Main Menu')
        mainB.action = lambda button: (game.reset(), game.main.setState(0))
        mainB.bColor = None
        Gui.addComponent(self, mainB)'''

        mainB = Button(grid.getRect(1, 2), 'Quite')
        mainB.action = lambda button: (game.main.exit())
        mainB.bColor = None
        Gui.addComponent(self, mainB)
