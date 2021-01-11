
import Tkinter as tk
import tkFont

from jlyreader import JLYFieldData
from core import JLYObject, String
from theme import colors, Color, amplifyColor as ac

def color(parent, data):
    return Color(parent, data).get()

#ComponentCount = 0
class JLYComponent(JLYObject):
    def __init__(self, parent, data, **kws):
        JLYObject.__init__(self, parent, **kws)
        self.content = []
        self.background = parent.background
        self.theme = parent.theme
        self.actionListener = parent.actionListener


        w = 100
        self.id = ''#srt(ComponentCount)
        for p in data.props:
            if p.name == 0:
                self.id = String(self, p.data).get()
                parent.addContent(self)
            if p.name == 'w':
                w = int(eval(p.data) * 100)

        self.frame = parent.getFrame(w=w)

    def addContent(self, child):
        self.content.append(child)
        self.parent.addContent(child)

    def focus(self, comp, foucused):
        self.parent.focus(comp, foucused)


class Button(JLYComponent):
    def __init__(self, parent, data, **kws):
        JLYComponent.__init__(self, parent, data, **kws)

        self.tkb = tk.Button(self.frame)
        self.tkb.config(command=lambda: self.actionListener(self))
        if data.oneline:
            self.tkb['text'] = data.data

        self.border = 'none'
        theme = self.theme.get('Button')
        if theme: self.readTheam(theme)
        self.readTheam(data.props)

        self.tkb.pack(fill=tk.BOTH, expand=1)

    def readTheam(self, fields):
        for f in fields:
            value = f.data
            name = f.name

            if ['tc', 'fg', 'textcolor', 'forgroundcolor'].__contains__(name):
                self.tkb['fg'] = Color(self, value).get()
            elif ['bg', 'background'].__contains__(name):
                self.background = Color(self, value).get()
                self.tkb['bg'] = self.background
                self.tkb['activebackground'] = ac(self.background, '#222222')
                if self.border == 'none':
                    self.tkb['highlightbackground'] = self.parent.background
            elif ['bw', 'borerwidth'].__contains__(name):
                self.tkb['bd'] = eval(value)
            elif ['border'].__contains__(name):
                if ['none', 'null'].__contains__(value):
                    self.border = 'none'
                    self.tkb['bd'] = 0
                    self.tkb['highlightbackground'] = self.parent.background
            elif ['font'].__contains__(name):
                font = tkFont.Font()
                f = value.split(',')
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
    def __init__(self, parent, data, **kws):
        JLYComponent.__init__(self, parent, data, **kws)

        self.tkl = tk.Label(self.frame)
        if data.oneline:
            self.tkl['text'] = data.data
            self.tkl['bg'] = self.background

        theme = self.theme.get('Label')
        if theme: self.readTheam(theme)
        self.readTheam(data.props)

        self.tkl.config(compound = tk.RIGHT)
        self.tkl.pack(fill=tk.BOTH, expand=1)

    def readTheam(self, fields):
        for f in fields:
            name = f.name; value = f.data

            if ['tc', 'fg', 'textcolor', 'forgroundcolor'].__contains__(name):
                self.tkl['fg'] = Color(self, value).get()
            elif ['align'].__contains__(name):
                self.tkl['justify'] = value
            elif ['bg', 'background'].__contains__(name):
                self.background = Color(self, value).get()
                self.tkl['bg'] = self.background
            elif ['border'].__contains__(name):
                if ['none', 'null'].__contains__(value):
                    self.border = 'none'
                    self.tkl['bd'] = 0
                    self.tkl['highlightbackground'] = self.parent.background
            elif ['font'].__contains__(name):
                font = tkFont.Font()
                f = value.split(',')
                if len(f) > 0: font.config(family=f[0])
                if len(f) > 1: font.config(size=eval(f[1]))
                #if ['b', 'bold', 'bi', 'bolditalic'].__contains__(f[2]):
                if len(f) > 2:
                    if f[2].__contains__('b'):
                        font.config(weight= f[2])
                    if f[2].__contains__('i'):
                        font.config(slant= f[2])
                self.tkl.config(font=font)

varletters = 'asdfghjklqwetyuiopzxcvbnm'

class Entry(JLYComponent):
    def focusIn(self, event):
        self.parent.focus(self, True)
    def focusOut(self, event):
        self.parent.focus(self, False)

    def __init__(self, parent, data, **kws):
        JLYComponent.__init__(self, parent, data, **kws)
        '''if p == 0:
            self.entries[data.props[p]] = tke
        '''

        text = String(self, data.data).get()

        self.tke = tk.Entry(self.frame)
        self.v = tk.StringVar()
        self.v.set(text)
        self.tke['textvariable'] = self.v

        self.tke.bind('<FocusIn>', self.focusIn )

        self.border = 'none'
        theme = self.theme.get('TField')
        if theme: self.readTheam(theme)
        self.readTheam(data.props)

        self.tke.pack(fill=tk.BOTH, expand=1)

    def set(self, key, value):
        if key == 'text':
            self.v.set(value)
        else:
            self.tke[key] = value

    def get(self, key):
        if key == 'text':
            return self.v.get()
        else:
            return self.tke.get(key)

    def readTheam(self, fields):
        for f in fields:
            name = f.name
            value = f.data#self.eval(f.data)

            if ['tc', 'fg', 'textcolor', 'forgroundcolor'].__contains__(name):
                self.tke['fg'] = color(self, value)
            elif ['align'].__contains__(name):
                self.tke['justify'] = value
            elif ['bg', 'background'].__contains__(name):
                self.background = Color(self, value).get()
                self.tke['bg'] = self.background
                if self.border == 'none':
                    self.tke['highlightbackground'] = self.parent.background
            elif ['bw', 'borerwidth'].__contains__(name):
                self.tke['bd'] = eval(value)
            elif ['border'].__contains__(name):
                if ['none', 'null'].__contains__(value):
                    self.border = 'none'
                    self.tke['bd'] = 0
                    self.tke['highlightbackground'] = self.parent.background
            elif ['font'].__contains__(name):
                font = tkFont.Font()
                f = value.split(',')
                if len(f) > 0: font.config(family=f[0])
                if len(f) > 1: font.config(size=eval(f[1]))
                if len(f) > 2:
                    if f[2].__contains__('b'):
                        font.config(weight= f[2])
                    if f[2].__contains__('i'):
                        font.config(slant= f[2])
                self.tke.config(font=font)
