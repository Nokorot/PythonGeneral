from Colors import *
from gui import *

from main import ScreenSize
#import options

from game import FiRGame

import RSA
import urllib2

class ServerClient():

    def __init__(self):
        self.url = 'http://127.0.0.1:5000/'

        self.rsa_server_public_key = self.request('public-rsa-key')
        self.rsa_private_keys = RSA.generate(1024)
        self.rsa_public_key = self.rsa_private_keys.publickey()
        self.rsa_packed_public_key = RSA.toMyBase(self.rsa_public_key.exportKey())

        self.url += '4inrow/'

    def request(self, s_url):
        return urllib2.urlopen(self.url + s_url).read()

    def encrypt(self, data):
        RSA.encrypt(data, self.rsa_server_public_key)

    def decrypt(self, data):
        RSA.decrypt(data, self.rsa_private_keys)


class MainMenu(Gui):

    def __init__(self, main):
        Gui.__init__(self, tuple(ScreenSize))

        self.serverClient = ServerClient()

        self.menu = None
        self.newGameMenu = NewGameMenu(self)
        self.connectMenu = ConnectMenu(self)

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

    def mainMenu(self):
        self.menu = None

    def makeNewGame(self):
        self.menu = self.newGameMenu

    def connectToGame(self, b=True):
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

    def eventHandeler(self, event):
        if self.menu != None:
            self.menu.eventHandeler(event)
        else:
            Gui.eventHandeler(self, event)

class NewGameMenu(Gui):
    def __init__(self, mainMenu):
        Gui.__init__(self, mainMenu.bounds())
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

        grid = self.getGrid([1,2,1],[2,0.5,1,0.5,1,1,1,2],10)
        #grid.getPos(1,1)

        gameL = Label(grid.getRect(1, 1), 'Game')
        self.addComponent(gameL)

        self.gameTF = TextField(grid.getRect(1, 2), 'game')
        self.addComponent(self.gameTF)

        sizeL = Label(grid.getRect(1, 3), 'Size')
        self.addComponent(sizeL)

        self.sizeTF = TextField(grid.getRect(1, 4), '7,5')
        self.addComponent(self.sizeTF)

        playB = Button(grid.getRect(1,5), 'Play')
        playB.action = lambda button: self.play()
        self.addComponent(playB)

        cancelB = Button(grid.getRect(1,6), 'Cancel')
        cancelB.action = lambda button: (mainMenu.mainMenu())
        self.addComponent(cancelB)

    def play(self):
        if (len(self.gameTF.name) < 3): return
        if (len(self.sizeTF.name) < 3): return
        game = FiRGame(self.mainMenu, self.gameTF.name, self.sizeTF.name)
        self.mainMenu.menu = game

class ConnectMenu(Gui):
    def __init__(self, mainMenu):
        Gui.__init__(self, mainMenu.bounds())

        grid = self.getGrid([1,2,1],[2,0.5,1,1,1,2],10)
        #grid.getPos(1,1)

        gameL = Label(grid.getRect(1, 1), 'Game')
        self.addComponent(gameL)

        gameTF = TextField(grid.getRect(1, 2))
        self.addComponent(gameTF)

        playB = Button(grid.getRect(1,3), 'Play')
        #playB.action = lambda button: (mainMenu)
        self.addComponent(playB)

        cancelB = Button(grid.getRect(1,4), 'Cancel')
        cancelB.action = lambda button: (mainMenu.mainMenu())
        self.addComponent(cancelB)
