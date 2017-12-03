from Colors import *
from gui import *

from main import ScreenSize
#import options

from game import MakeFiRGame, ConnectFiRGame

import pygame
import RSA
import urllib2

class ServerClient():
    def __init__(self):
        self.url = 'http://127.0.0.1:5000/'
        #self.url = 'http://127.0.0.1:8000/'
        #self.url = 'https://minigameshost.herokuapp.com/'

        private, public = RSA.generate(1024)
        self.rsa_private_keys = private
        self.rsa_public_key = public

        self.rsa_server_public_key = self.request('public-rsa-key')
        print self.rsa_public_key
        self.online = self.rsa_public_key != None

        self.url += '4inrow/'

    def request(self, s_url):
        try:
            return urllib2.urlopen(self.url + s_url).read()
        except:
            return None

    def encrypt(self, data):
        return RSA.encrypt(data, self.rsa_server_public_key)

    def decrypt(self, data):
        return RSA.decrypt(data, self.rsa_private_keys)

class MainMenu(Gui):

    def __init__(self, main):
        Gui.__init__(self, tuple(ScreenSize))

        self.name = "User"

        self.serverClient = ServerClient()

        self.signInMenu = SignInMenu(self)
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
        self.onlineL = Label(rec, 'Online')
        self.addComponent(self.onlineL)

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
        self.gameTF.action = lambda tf: self.play()
        self.addComponent(self.gameTF)

        sizeL = Label(grid.getRect(1, 3), 'Size')
        self.addComponent(sizeL)

        self.sizeTF = TextField(grid.getRect(1, 4), '7,5')
        self.sizeTF.action = lambda tf: self.play()
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

        game = self.gameTF.name
        size = self.sizeTF.name

        self.mainMenu.menu = MakeFiRGame(self.mainMenu, game, size)

class ConnectMenu(Gui):
    def __init__(self, mainMenu):
        Gui.__init__(self, mainMenu.bounds())

        self.mainMenu = mainMenu
        self.serverClient = mainMenu.serverClient

        grid = self.getGrid([1,2,1],[2,0.5,1,1,1,2],10)
        #grid.getPos(1,1)

        gameL = Label(grid.getRect(1, 1), 'Game')
        self.addComponent(gameL)

        self.gameTF = TextField(grid.getRect(1, 2))
        self.gameTF.action = lambda tf: self.play()
        self.addComponent(self.gameTF)

        playB = Button(grid.getRect(1,3), 'Play')
        playB.action = lambda button: ( self.play() )
        self.addComponent(playB)

        cancelB = Button(grid.getRect(1,4), 'Cancel')
        cancelB.action = lambda button: ( mainMenu.mainMenu() )
        self.addComponent(cancelB)

    def play(self):
        if (len(self.gameTF.name) < 3): return

        game = self.gameTF.name

        self.mainMenu.menu = ConnectFiRGame(self.mainMenu, game)
