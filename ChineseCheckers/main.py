#!/usr/bin/python

import os, sys
sys.path.insert(0, os.path.abspath('utils'))
sys.path.insert(0, os.path.abspath('quark'))
sys.path.insert(0, os.path.abspath('quark/guis'))

from gameMain import GameMain

from vec import *
ScreenWidth = 800;
ScreenHeight = 600;
ScreenSize = Vec(ScreenWidth, ScreenHeight)

import menu_main as mm
from serverClient import ServerClient
import game

if __name__ == '__main__':

    def init(main):
        main.serverClient = ServerClient()
        main.serverClient.start(1/5.)
        #return game.Game(main)
        return mm.MainMenu(main)

    main = GameMain(init, ScreenSize.floor())
    main.start()
    serverClient.stop()
