
import Tkinter as tk

All = 'nwse'

from core import JLYObject
from component import JLYComponent

class X(JLYComponent):
    def __init__(self, parent, data, **kws):
        JLYComponent.__init__(self, parent, data, **kws)

        self.xg = tk.Frame(self.frame)
        self.xg.pack(side=tk.TOP, expand=1, padx=0, pady=0, fill=tk.BOTH)
        self.xg['bg'] = self.background

        self.xpad = 3;
        self.ypad = 3;

        theme = self.theme.get('X')
        if theme:
            self.readTheam(theme)
        self.readTheam(data.props)

        tk.Grid.rowconfigure(self.xg, 0, weight=1)

        if data.oneline:
            return
            #data.readLine()

        self.x = 0
        for e in data.elements:
            if e.dType == 'object':
                if self.Objects.__contains__(e.name):
                    self.Objects[e.name](self, e)

    def getFrame(self, w=100):
        self.xg.columnconfigure(self.x, weight=w)

        f = tk.Frame(self.xg)
        f.pack_propagate(False)

        f.grid(row=0, column=self.x, sticky=All, padx=self.xpad, pady=self.ypad)
        f['bg'] = self.background

        self.x += 1
        return f

    def readTheam(self, fields):
        for f in fields:
            value = f.data#self.eval(f.data)

            if ['space'].__contains__(f.name):
                self.xpad = self.ypad = value


class Y(JLYComponent):
    def __init__(self, parent, data, **kws):
        JLYComponent.__init__(self, parent, data, **kws)

        self.yg = tk.Frame(self.frame)
        self.yg.pack(side=tk.LEFT, expand=1, padx=0, pady=0, fill=tk.BOTH)
        self.yg['bg'] = self.background

        tk.Grid.columnconfigure(self.yg, 0, weight=1)

        if data.oneline:
            return
            #data.readLine()

        self.y = 0
        for e in data.elements:
            if e.dType == 'object':
                if self.Objects.__contains__(e.name):
                    self.Objects[e.name](self, e)

    def getFrame(self, w=100):
        self.yg.rowconfigure(self.y, weight=w)

        f = tk.Frame(self.yg)
        f.pack_propagate(False)
        f.grid(row=self.y, column=0, sticky=All)
        f['bg'] = self.background

        self.y += 1
        return f
