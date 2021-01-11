from Colors import *
from gui import *

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

class OptionMenu(Gui):
    def __init__(self, mainMenu):
        Gui.__init__(self, mainMenu.bounds())

        grid = self.getGrid([1,2,1], [2,1,1,1,2], 10)

        name = TextField(grid.getRect(1,1), '')
        #name.action = lambda button: (mainMenu.openOptionMenu(False))
        self.addComponent(name)

        diffic = Glider(grid.getRect(1,2), '')
        diffic.action = None
        self.addComponent(diffic)

        backB = Button(grid.getRect(1,3), 'Back')
        backB.action = lambda button: (mainMenu.openOptionMenu(False))
        self.addComponent(backB)
