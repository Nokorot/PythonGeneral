
from core import JLYObject

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
        return self.theams[name]

    def build(self, data):
        for f in data.fields:
            self.theams[f.name] = f.data

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
