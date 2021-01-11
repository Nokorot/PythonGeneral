
class JLYObject:
    def __init__(self, parent, **kws):
        self.parent = parent
        self.Objects = parent.Objects
        self.vars = parent.vars

        for kw in kws:
            if kw == 'vars':
                vars = kws[kw]
                for v in vars:
                    self.vars[v] = vars[v]
                #self.vars += ..

from theme import colors

class Body(JLYObject):
    def __init__(self, parent):
        JLYObject.__init__(self, parent)
        self.actionListener = parent.actionListener
        self.theme = parent.theme
        self.background = colors['light_grey']

    def build(self, data):
        for o in data.objects:
            if self.Objects.__contains__(o.name):
                self.Objects[o.name](o, self)

    def getFrame(self, **kws):
        return self.parent.frame

class Head(JLYObject):
    def __init__(self, parent):
        JLYObject.__init__(self, parent)

    def build(self, data):
        root = self.parent.root

        width = '600'; height='400';
        minw = 600; minh = 400;
        maxw = 600; maxh = 400
        for f in data.fields:
            if f.name == 'title':
                root.title(f.data)
            if f.name == 'resizeable':
                b = f.data == 'true'
                root.resizable(width=b, height=b)
            if f.name == 'size':
                s = f.data.split(',')
                root.geometry('%sx%s' % (eval(s[0]), eval(s[1])))
            if f.name == 'width':
                width = f.data
                root.geometry('%sx%s' % (eval(width), eval(height)))
            if f.name == 'height':
                height = f.data
                root.geometry('%sx%s' % (eval(width), eval(height)))
            if f.name == 'minsize':
                s = f.data.split(',')
                root.minsize(eval(s[0]), eval(s[1]))
            if f.name == 'minwidth':
                minw = int(f.data)
                root.minsize(minw, minh)
            if f.name == 'minheight':
                minh = int(f.data)
                root.minsize(minw, minh)
            if f.name == 'maxsize':
                s = f.data.split(',')
                root.maxsize(eval(s[0]), eval(s[1]))
            if f.name == 'maxwidth':
                maxw = eval(f.data)
                root.minsize(maxw, maxh)
            if f.name == 'maxheight':
                maxh = eval(f.data)
                root.minsize(maxw, maxh)
            if f.name == 'background':
                root.wait_visibility(root)
                #root.wm_attributes("-alpha", 0.8)
                self.parent.body.background = [colors[f.data]]
                self.parent.frame['bg'] = colors[f.data]

class For(JLYObject):
    def __init__(self, data, parent):
        JLYObject.__init__(self, parent)

        if data.oneline:
            return
            #data.readLine()

        var = data.props[0]
        bexp = data.props[1]
        end = data.props[2]

        v = var.split('=')
        if len(v) > 1:
            exec var
        v = v[0]

        while eval(bexp):
            for o in data.objects:
                if self.Objects.__contains__(o.name):
                    self.Objects[o.name](o, parent, vars={v:eval(v)})
                exec end
