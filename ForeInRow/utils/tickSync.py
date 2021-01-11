
from threading import Thread
from time import time, sleep

class Sync():
    def __init__(self, func, ups):
        self.func = func
        self.ups = ups
        self.run = False

    def start(self):
        self.run = True
        while self.run:
            lastTime = time()
            self.func()
            delay = max( 0, (lastTime + self.ups) - time())
            sleep(delay)

    def stop(self):
        self.run = False
