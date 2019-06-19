from Colors import *
from gui import *

import options

class MainMenu(Gui):

    def __init__(self, main):
        Gui.__init__(self, (main.width, main.height))

        grid = self.getGrid([1,2,1],[2,1,1,1,2],10)
        #grid.getPos(1,1)

        self.options = False
        self.optionMenu = OptionMenu(self)

        startB = Button(grid.getRect(1,1), 'Start')
        startB.action = lambda button: (main.setState(1))
        self.addComponent(startB)

        optionB = Button(grid.getRect(1,2), 'Options')
        optionB.action = lambda button: (self.openOptionMenu(True))
        self.addComponent(optionB)

        quiteB = Button(grid.getRect(1,3), 'Quite')
        quiteB.action = lambda button: (main.exit())
        self.addComponent(quiteB)

    def openOptionMenu(self, b=True):
        self.options = b

    def update(self):
        if self.options:
            self.optionMenu.update()
        else:
            Gui.update(self)

    def render(self, screen):
        if self.options:
            self.optionMenu.render(screen)
        else:
            Gui.render(self, screen)

    def eventCathcer(self, event):
        if self.options:
            self.optionMenu.eventCathcer(event)
        else:
            Gui.eventCathcer(self, event)


def c(c):
    (options.setColor(c.value))

def drawLabel(screen, c):
    snake = options.snake
    if snake:
        a, b = c.rect.getPos()
        w, h = snake[2].get_size()
        screen.blit(snake[1], (a, b))
        screen.blit(snake[2], (a + w, b))
        screen.blit(snake[0], (a + w * 2, b))

class OptionMenu(Gui):
    def __init__(self, mainMenu):
        Gui.__init__(self, mainMenu.bounds())

        grid = self.getGrid([1,2,1], [1,2,1,1,2], 10)

        g0 = grid.getRect(1, 1).getGrid([3,1], 1, 0)

        '''scolor = Colorrect(g0.getRect(0,0))
        scolor.gliderOrientation('left')
        scolor.value = (100,200,50)
        scolor.action = c #lambda c: (options.setColor(c.value))
        self.addComponent(scolor)'''

        label = Label(g0.getRect(1, 0))
        label.draw = drawLabel
        self.addComponent(label)

        backB = Button(grid.getRect(1,3), 'Back')
        backB.action = lambda button: (mainMenu.openOptionMenu(False))
        self.addComponent(backB)

        def action(g):
            print(g.value())
            options.dificolty = g.value()

        diffic = Glider(grid.getRect(1,2), '', values=range(1,5+1))
        diffic.action = action
        self.addComponent(diffic)
