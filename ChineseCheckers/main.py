#!/usr/bin/python

import os, sys
sys.path.insert(0, os.path.abspath('utils'))
sys.path.insert(0, os.path.abspath('quark'))
sys.path.insert(0, os.path.abspath('quark/guis'))

from gameMain import GameMain

from vec import *
ScreenWidth = 800;
ScreenHeight = 700;
ScreenSize = Vec(ScreenWidth, ScreenHeight)

import menu_main as mm
import game

if __name__ == '__main__':

    def init(main):

        #return game.Game(main)
        return mm.MainMenu(main)

    main = GameMain(init, ScreenSize.floor())
    main.start()
