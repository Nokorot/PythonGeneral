
import Tkinter as tk
import tkFont

from jlyreader import JLYFieldData
from core import JLYObject
from theme import colors, amplifyColor as ac

class JLYComponent(JLYObject):
    def __init__(self, data, parent, **kws):
        JLYObject.__init__(self, parent, **kws)
        self.background = parent.background
        self.theme = parent.theme
        self.actionListener = parent.actionListener

        w = 100
        self.id = ''#srt(ComponentCount)
        for p in data.props:
            if p == 0:
                self.id = data.props[p]
                #parent.add(id, self)
            if p == 'w':
                w = int(eval(data.props[p]) * 100)

        self.frame = parent.getFrame(w=w)



class Button(JLYComponent):
    def __init__(self, data, parent, **kws):
        JLYComponent.__init__(self, data, parent, **kws)

        self.tkb = tk.Button(self.frame)
        self.tkb.config(command=lambda: self.actionListener(self.id))
        if data.oneline:
            self.tkb['text'] = data.data

        self.border = 'none'
        self.readTheam(self.theme.get('Button'))
        self.readTheam(data.props)

        self.tkb.pack(fill=tk.BOTH, padx = 3, pady=3, expand=1)

    def readTheam(self, fields):
        for f in fields:
            if ['tc', 'fg', 'textcolor', 'forgroundcolor'].__contains__(f):
                self.tkb['fg'] = colors[fields[f]]
            elif ['bg', 'background'].__contains__(f):
                self.background = colors[fields[f]]
                self.tkb['bg'] = self.background
                self.tkb['activebackground'] = ac(self.background, '#222222')
                if self.border == 'none':
                    self.tkb['highlightbackground'] = self.parent.background
            elif ['bw', 'borerwidth'].__contains__(f):
                self.tkb['bd'] = eval(fields[f])
            elif ['border'].__contains__(f):
                if ['none', 'null'].__contains__(fields[f]):
                    self.border = 'none'
                    self.tkb['bd'] = 0
                    self.tkb['highlightbackground'] = self.parent.background
            elif ['font'].__contains__(f):
                font = tkFont.Font()
                f = fields[f].split(',')
                if len(f) > 0: font.config(family=f[0])
                if len(f) > 1: font.config(size=eval(f[1]))
                #if ['b', 'bold', 'bi', 'bolditalic'].__contains__(f[2]):
                if len(f) > 2:
                    if f[2].__contains__('b'):
                        font.config(weight= f[2])
                    if f[2].__contains__('i'):
                        font.config(slant= f[2])
                self.tkb.config(font=font)

class Label(JLYComponent):
    def __init__(self, data, parent, **kws):
        JLYComponent.__init__(self, data, parent, **kws)

        tkl = tk.Label(self.frame)
        if data.oneline:
            tkl['text'] = data.data
            tkl['bg'] = self.background
        for p in data.props:
            if ['tc', 'fg', 'textcolor', 'foregroundcolor'].__contains__(p):
                tkl['fg'] = colors[data.props[p]]
        tkl.config(compound = tk.RIGHT)
        tkl.pack(fill=tk.BOTH, padx=3, pady=3, expand=1)

varletters = 'asdfghjklqwetyuiopzxcvbnm'

class Entry(JLYComponent):
    def __init__(self, data, parent, **kws):
        JLYComponent.__init__(self, data, parent, **kws)

        '''if p == 0:
            self.entries[data.props[p]] = tke'''


        text = data.data
        if text.__contains__('%'):
            out = ''
            par = False; vardata = ''
            for c in data.data:
                if c == '%':
                    par = True
                elif par:
                    if not varletters.__contains__(c.lower()):
                        if self.vars.__contains__(vardata):
                            out += str(self.vars[vardata])
                        par = False
                        out += c
                        vardata = ''
                    else:
                        vardata += c
                else:
                    out += c
            if par:
                if self.vars.__contains__(vardata):
                    out += str(self.vars[vardata])
                par = False
                vardata = ''
            text = out


        self.tke = tk.Entry(self.frame)
        v = tk.StringVar()
        v.set(text)
        self.tke['textvariable'] = v

        self.border = 'none'
        self.readTheam(self.theme.get('TField'))
        self.readTheam(data.props)

        self.tke.pack(fill=tk.BOTH, padx=3, pady=3, expand=1)

    def readTheam(self, fields):
        for f in fields:
            if ['tc', 'fg', 'textcolor', 'forgroundcolor'].__contains__(f):
                self.tke['fg'] = colors[fields[f]]
            elif ['align'].__contains__(f):
                self.tke['justify'] = fields[f]
            elif ['bg', 'background'].__contains__(f):
                self.background = colors[fields[f]]
                self.tke['bg'] = self.background
                if self.border == 'none':
                    self.tke['highlightbackground'] = self.parent.background
            elif ['bw', 'borerwidth'].__contains__(f):
                self.tke['bd'] = eval(fields[f])
            elif ['border'].__contains__(f):
                if ['none', 'null'].__contains__(fields[f]):
                    self.border = 'none'
                    self.tke['bd'] = 0
                    self.tke['highlightbackground'] = self.parent.background
            elif ['font'].__contains__(f):
                font = tkFont.Font()
                f = fields[f].split(',')
                if len(f) > 0: font.config(family=f[0])
                if len(f) > 1: font.config(size=eval(f[1]))
                #if ['b', 'bold', 'bi', 'bolditalic'].__contains__(f[2]):
                if len(f) > 2:
                    if f[2].__contains__('b'):
                        font.config(weight= f[2])
                    if f[2].__contains__('i'):
                        font.config(slant= f[2])
                self.tke.config(font=font)
