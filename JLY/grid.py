
import Tkinter as tk

All = 'nwse'

from core import JLYObject
from component import JLYComponent

class X(JLYComponent):
    def __init__(self, data, parent, **kws):
        JLYComponent.__init__(self, data, parent, **kws)

        self.xg = tk.Frame(self.frame)
        self.xg.pack(side=tk.TOP, expand=1, padx=0, pady=0, fill=tk.BOTH)
        self.xg['bg'] = self.background

        tk.Grid.rowconfigure(self.xg, 0, weight=1)

        if data.oneline:
            return
            #data.readLine()

        self.x = 0
        for o in data.objects:
            if self.Objects.__contains__(o.name):
                self.Objects[o.name](o, self)

    def getFrame(self, w=100):
        self.xg.columnconfigure(self.x, weight=w)

        f = tk.Frame(self.xg)
        f.pack_propagate(False)
        f.grid(row=0, column=self.x, sticky=All)
        f['bg'] = self.background

        self.x += 1
        return f

class Y(JLYComponent):
    def __init__(self, data, parent, **kws):
        JLYComponent.__init__(self, data, parent, **kws)

        self.yg = tk.Frame(self.frame)
        self.yg.pack(side=tk.LEFT, expand=1, padx=0, pady=0, fill=tk.BOTH)
        self.yg['bg'] = self.background

        tk.Grid.columnconfigure(self.yg, 0, weight=1)

        if data.oneline:
            return
            #data.readLine()

        self.y = 0
        for o in data.objects:
            if self.Objects.__contains__(o.name):
                self.Objects[o.name](o, self)

    def getFrame(self, w=100):
        self.yg.rowconfigure(self.y, weight=w)

        f = tk.Frame(self.yg)
        f.pack_propagate(False)
        f.grid(row=self.y, column=0, sticky=All)
        f['bg'] = self.background

        self.y += 1
        return f
