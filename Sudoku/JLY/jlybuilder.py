
from jlyreader import *
from Tkinter import *

from core import *
from theme import Theme, colors

from grid import X, Y
from component import Button, Label, Entry
from theme import Color


Alpha1 = {'X': X, 'Y': Y, 'for': For,
    'Button': Button, 'Label': Label, 'Entry':Entry,'TextField': Entry,
    'Color': Color, 'color': Color, 'Colour': Color, 'colour': Color,
    'str': String, 'int': Int }

def keypress(event):
    print event

class JLYFrame:

    def __init__(self, filename, Objects=Alpha1):
        self.Objects = Objects

        self.actionListeners = []
        self.vars = {}

        self.jlyreader = JLYReader(filename)
        self.jlyreader.read()

        self.input  = Input(self)
        self.theme  = Theme(self)
        self.head   = Head(self)
        self.body   = Body(self)

        self.input.build(self.jlyreader.get('In'))

    def build(self):
        get = self.jlyreader.get

        self.root = Tk()
        self.frame=Frame(self.root)
        self.frame.pack(fill=BOTH, expand=1)

        '''self.buttons = {}
        self.labels = {}
        self.entries = {}'''

        for e in self.jlyreader.elements:
            if e.dType == 'object':
                if self.Objects.__contains__(e.name):
                    self.Objects[e.name](self, e)

        self.theme.build(get('Theme'))
        self.head.build(get('Head'))
        self.body.build(get('Body'))

        return self

    def getComponent(self, label):
        for comp in self.body.content:
            if comp.id == label:
                return comp

    def actionListener(self, comp):
        for listener in self.actionListeners:
            listener(comp)

    def run(self):
        self.root.mainloop()

    def open(self):
        #self.thread = Thread(target=self.run)
        #self.thread.start()
        self.root.mainloop()

    def bindInput(self, key, value):
        self.vars[key].set(value)



if __name__ == "__main__":
    frame = JLYFrame('MainMenu.jly')
    frame.build()
    frame.open()
