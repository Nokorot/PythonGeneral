
import pygame


from Colors import *
from gui import *

from main import ScreenSize
#import options

from game import MakeNewGame, ConnectToGame

class MainMenu(Gui):

    def __init__(self, main):
        Gui.__init__(self, main, tuple(ScreenSize))

        self.name = "User"

        self.serverClient = main.serverClient

        #self.signInMenu = SignInMenu(self)
        self.newGameMenu = NewGameMenu(self)
        self.connectMenu = ConnectMenu(self)
        self.menu = None #self.signInMenu

        grid = self.getGrid([1,2,1],[2,1,1,1,2],10)

        newGameB = Button(grid.getRect(1,1), 'New Game')
        newGameB.action = lambda button: (self.makeNewGame())
        self.addComponent(newGameB)

        connectB = Button(grid.getRect(1,2), 'Connect To Game')
        connectB.action = lambda button: (self.connectToGame())
        self.addComponent(connectB)

        quiteB = Button(grid.getRect(1,3), 'Quite')
        quiteB.action = lambda button: (main.exit())
        self.addComponent(quiteB)

        rec = Rectangle((self.width - 150, 10, 140, 30))
        text = 'Online!' if self.serverClient.online else 'Offline!'
        self.onlineL = Label(rec, text)
        self.onlineL.fColor = green if self.serverClient.online else red
        self.addComponent(self.onlineL)

    def mainMenu(self):
        self.menu = None

    def makeNewGame(self):
        if self.serverClient.online:
            self.menu = self.newGameMenu

    def connectToGame(self, b=True):
        if self.serverClient.online:
            self.menu = self.connectMenu

    def update(self):
        if self.menu != None:
            self.menu.update()
        else:
            Gui.update(self)

    def render(self, screen):
        if self.menu != None:
            self.menu.render(screen)
        else:
            Gui.render(self, screen)

    def eventAction(self, event):
        if self.menu != None:
            self.menu.eventAction(event)
        else:
            Gui.eventAction(self, event)

class SignInMenu(Gui):
    def __init__(self, mainMenu):
        Gui.__init__(self, mainMenu.bounds())

        self.mainMenu = mainMenu
        self.serverClient = mainMenu.serverClient

        grid = self.getGrid([1, 2, 1], [2, 0.5, 1, 1, 2], 10)

        nameL = Label(grid.getRect(1, 1), 'Name')
        self.addComponent(nameL)

        self.nameTF = TextField(grid.getRect(1, 2))
        self.addComponent(self.nameTF)

        signInB = Button(grid.getRect(1, 3), 'Sign In')
        signInB.action = lambda button: self.signIn();
        self.addComponent(signInB)

    def eventHandeler(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                self.signIn()
                return
        Gui.eventHandeler(self, event)

    def signIn(self):
        if (len(self.nameTF.name) < 3): return
        self.mainMenu.name = self.nameTF.name
        self.mainMenu.menu = None

class NewGameMenu(Gui):
    def __init__(self, mainMenu):
        Gui.__init__(self, mainMenu, mainMenu.bounds())
        '''
        <X, spacing:10>{
            <Space, w:2>
            <Label, w:0.5, spacing_S:1> Game
            <TextField, game>
            <Label, w:0.5, spacing_S:1> Size
            <TextField, size>
            <Button, play> Play
            <Button, cancel> Cancel
            <Space, w:2>
        }
        '''

        self.mainMenu = mainMenu
        self.serverClient = mainMenu.serverClient

        grid = self.getGrid([1,2,1],[2,1,1,1,2],10)
        #grid.getPos(1,1)

        '''gameL = Label(grid.getRect(1, 1), 'Game')
        self.addComponent(gameL)
        '''

        self.gameTF = TextField(grid.getRect(1, 1), 'game')
        self.gameTF.action = lambda tf: self.play()
        self.addComponent(self.gameTF)

        '''sizeL = Label(grid.getRect(1, 3), 'Size')
        self.addComponent(sizeL)

        self.sizeTF = TextField(grid.getRect(1, 4), '7,5')
        self.sizeTF.action = lambda tf: self.play()
        self.addComponent(self.sizeTF)'''

        playB = Button(grid.getRect(1,2), 'Play')
        playB.action = lambda button: self.play()
        self.addComponent(playB)

        cancelB = Button(grid.getRect(1,3), 'Cancel')
        cancelB.action = lambda button: (mainMenu.mainMenu())
        self.addComponent(cancelB)

    def play(self):
        if (len(self.gameTF.name) < 3): return
        #if (len(self.sizeTF.name) < 3): return

        game = self.gameTF.name
        #size = self.sizeTF.name

        self.mainMenu.menu = None
        self.mainMenu.menu = MakeNewGame(self.mainMenu, game)

class ConnectMenu(Gui):
    def __init__(self, mainMenu):
        Gui.__init__(self, mainMenu, mainMenu.bounds())

        self.mainMenu = mainMenu
        self.serverClient = mainMenu.serverClient

        grid = self.getGrid([1,2,1],[2,0.5,1,1,1,2],10)
        #grid.getPos(1,1)

        gameL = Label(grid.getRect(1, 1), 'Game')
        self.addComponent(gameL)

        self.gameTF = TextField(grid.getRect(1, 2), 'game')
        self.gameTF.action = lambda tf: self.play()
        self.addComponent(self.gameTF)

        playB = Button(grid.getRect(1,3), 'Play')
        playB.action = lambda button: ( self.play() )
        self.addComponent(playB)

        cancelB = Button(grid.getRect(1,4), 'Cancel')
        cancelB.action = lambda button: ( mainMenu.mainMenu() )
        self.addComponent(cancelB)

    def play(self):
        print 'Hey'

        if (len(self.gameTF.name) < 3): return

        print 'Hey'

        game = self.gameTF.name

        self.mainMenu.menu = ConnectToGame(self.mainMenu, game)
