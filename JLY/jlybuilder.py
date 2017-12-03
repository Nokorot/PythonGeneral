
from jlyreader import *
from Tkinter import *

from core import *
from theme import Theme, colors

from grid import X, Y
from component import Button, Label, Entry


Alpha1 = {'X': X, 'Y': Y, 'for': For,
    'Button': Button, 'Label': Label, 'Entry':Entry,'TextField': Entry }

class JLYFrame:
    def __init__(self, filename, Objects=Alpha1):
        self.Objects = Objects
        self.vars = {}
        self.jlyreader = JLYReader(filename)
        self.actionListeners = []

        self.head = Head(self)
        self.theme = Theme(self)
        self.body = Body(self)

    def build(self):
        self.jlyreader.read()
        #self.jlyreader.show()

        self.root = Tk()
        self.frame=Frame(self.root)
        self.frame.pack(fill=BOTH, expand=1)

        self.buttons = {}
        self.labels = {}
        self.entries = {}

        for o in self.jlyreader.objects:
            if o.name == 'head':
                self.head.build(o)
            elif o.name == 'body':
                self.body.build(o)
            elif o.name == 'theme':
                self.theme.build(o)

    def actionListener(self, comp):
        #print comp
        for listener in self.actionListeners:
            listener(comp)

    def run(self):
        self.root.mainloop()

    def open(self):
        #self.thread = Thread(target=self.run)
        #self.thread.start()
        self.root.mainloop()






if __name__ == "__main__":
    frame = JLYFrame('MainMenu.jly')
    frame.build()
    frame.open()
