
from core import JLYObject, String

colors = {
    'black'       : '#000000',
    'white'       : '#ffffff',
    'red'         : '#ff0000',
    'green'       : '#00ff00',
    'blue'        : '#0000ff',
    'yellow'      : '#ffff00',
    'pink'        : '#ff00ff',
    'cyan'        : '#00ffff',
    'grey'        : '#777777',
    'light_grey'  : '#aaaaaa',
    'dark_grey'   : '#333333',
}

class Theme(JLYObject):
    def __init__(self, parent):
        JLYObject.__init__(self, parent)
        self.theams = {}

    def get(self, name):
        if self.theams.__contains__(name):
            return self.theams[name]
        return None

    def build(self, data):
        for e in data.elements:
            if e.dType == 'object':
                self.Objects[e.name](self, e)
            elif e.dType == 'field':
                self.theams[e.name] = e.elements

class Color(JLYObject):
    def __init__(self, parent, data, name=None, **kws):
        JLYObject.__init__(self, parent, **kws)

        if type(data) == str:
            self.value = self.parse(data)
            return

        for p in data.props:
            if p.name == 0:
                self.id = String(self, p.data).get()
                self.parent.vars[self.id] = self


        self.value = self.parse(data.data)


    def parse(self, inp):
        value = self.eval(inp)

        #print value, inp

        for var in self.vars:
            if var == value:
                return self.vars[var].get()

        if colors.__contains__(value):
            return colors[value]
        elif value=='None':
            return None
        else:
            return value

    def get(self):
        return self.value


def clamp(c):
    return max(min(c, 255), 0)

def reduseColor(color, amount):
    r = eval('0x' + color[1:3])
    g = eval('0x' + color[3:5])
    b = eval('0x' + color[5:7])
    rr = eval('0x' + amount[1:3])
    gr = eval('0x' + amount[3:5])
    br = eval('0x' + amount[5:7])
    return '#%.2x%.2x%.2x' % (clamp(r-rr), clamp(g-gr), clamp(b-br))

def amplifyColor(color, amount):
    r = eval('0x' + color[1:3])
    g = eval('0x' + color[3:5])
    b = eval('0x' + color[5:7])
    rr = eval('0x' + amount[1:3])
    gr = eval('0x' + amount[3:5])
    br = eval('0x' + amount[5:7])
    return '#%.2x%.2x%.2x' % (clamp(r+rr), clamp(g+gr), clamp(b+br))
'''
class ComponentTheme:
    def __init__(self, )
    data = {}


class ButtonTheme:
'''
