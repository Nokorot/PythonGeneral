
from threading import Thread, current_thread
from time import time, sleep

class Sync():
    def __init__(self, func, ups):
        self.func = func
        self.ups = ups
        self.run = False

    def sync(self):
        self.run = True
        while self.run:
            lastTime = time()
            self.func()
            delay = max( 0, (lastTime + self.ups) - time())
            sleep(delay)

    def stop(self):
        self.run = False

class ThreadedSync(Sync):

    def sync(self):
        if self.run:
            return
        self.run = True

        self.parrentThread = current_thread()
        def run():
            while self.run:
                if not self.parrentThread.isAlive():
                    self.stop(); return
                lastTime = time()
                self.func()
                delay = max( 0, (lastTime + self.ups) - time())
                sleep(delay)

        thread = Thread(target = run)
        thread.start()
