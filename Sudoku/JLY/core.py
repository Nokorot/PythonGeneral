
letters = 'qwertyuiopasdfghjklzxcvbnm'

class StringReader():
    def __init__(self, data):
        self.index = -1
        self.data = data

    def next(self):
        self.index += 1
        if len(self.data) <= self.index:
            return None
        self.c = self.data[self.index]
        return self.c

class JLYObject:
    def __init__(self, parent, **kws):
        self.parent = parent
        self.Objects = parent.Objects
        self.vars = parent.vars

        self.childs = []
        #self.parent.addChild(self)

        for kw in kws:
            if kw == 'vars':
                vars = kws[kw]
                for v in vars:
                    self.vars[v] = vars[v]
                #self.vars += ..

    def addChild(self, child):
        self.childs.append(child)

    def eval(self, data):
        import re


        for e in re.findall(r"[\w']+", data):
            try:
                float(e)
            except:
                if self.vars.__contains__(e):
                    try:
                        var = self.vars[e]
                        if isinstance(var, JLYObject):
                            var = var.get()
                        exec (str(e)+'='+str(var))
                    except:
                        data = data.replace(e, "'%s'" % e)

                    #TODO : use this
                    '''
                    exec (str(e)+'='+str(self.vars[e].get()))
                    '''

                elif ['if', 'else', 'and', 'or'].__contains__(e):
                    pass
                else:
                    data = data.replace(e, "'%s'" % e)

        data.replace('?', 'if')
        data.replace(':', 'else')
        data.replace('||', 'or')
        data.replace('&&', 'and')

        try:
            return eval(data)
        except NameError:
            return eval('"%s"' % data)
        except:
            return data

        # TODO: make this not shit!!

    def execute(self, data):
        def split(key):
            A = data.split(key, 1)
            id = A[0].replace(' ', '')
            value = self.eval(A[1])
            return id, value

        if  data.__contains__('+='):
            id, value = split('+=')
            self.vars[id].value += value
        elif data.__contains__('-='):
            id, value = split('-=')
            self.vars[id].value -= value
        elif data.__contains__('*='):
            id, value = split('*=')
            self.vars[id].value *= value
        elif data.__contains__('/='):
            id, value = split('/=')
            self.vars[id].value /= value
        elif data.__contains__('%='):
            id, value = split('%=')
            self.vars[id].value %= value
        elif data.__contains__('='):
            id, value = split('=')
            self.vars[id].value = value


        # TODO: make this not shit!!

class String(JLYObject):
    def __init__(self, parent, data, **kws):
        JLYObject.__init__(self, parent, **kws)

        if type(data) == str:
            self.value = self.parse(data)
            return

        for p in data.props:
            if p.name == 0:
                self.id = String(self, p.data).get()
                parent.vars[self.id] = self

        self.value = self.parse(data.data)

    def parse(self, data):
        out = self.eval(data)

        if type(out) != str:
            return ''

        sr = StringReader(out)

        out = ''
        while sr.next():
            if sr.c == '%':
                v = ''
                while sr.next():
                    if letters.__contains__(sr.c.lower()):
                        v += sr.c
                        if self.vars.__contains__(v):
                            out += str(self.vars[v])
                        else:
                            out += '#%s#' % v
                    else:
                        out += sr.c
                        break
            else:
                out += sr.c
        return out

    def set(self, value):
        self.value = str(value)

    def get(self):
        return self.value

class Int(JLYObject):
    def __init__(self, parent, data, **kws):
        JLYObject.__init__(self, parent, **kws)

        if type(data) == str:
            self.value = self.parse(data)
            return

        for p in data.props:
            if p.name == 0:
                self.id = String(self, p.data).get()
                self.parent.vars[self.id] = self

        self.value = self.parse(data.data)

    def parse(self, data):
        return int(self.eval(data))

    def set(self, value):
        self.value = int(value)

    def get(self):
        return self.value

    def __str__(self):
        return str(self.value)

class Float(JLYObject):
    def __init__(self, parent, data, **kws):
        JLYObject.__init__(self, parent, **kws)

        if type(data) == str:
            self.value = self.parse(data)
            return

        for p in data.props:
            if p.name == 0:
                self.id = String(self, p.data).get()
                self.parent.vars[self.id] = self

        self.value = self.parse(data.data)

    def parse(self, data):
        return self.eval(data)

    def set(self, value):
        self.value = float(value)

    def get(self):
        return self.value

    def __str__(self):
        return str(self.value)

from theme import Color

class Input(JLYObject):
    def __init__(self, parent):
        JLYObject.__init__(self, parent)

    def build(self, data):
        for e in data.elements:
            if e.dType == 'field':
                pass
            elif e.dType == 'object':
                if e.dType == 'object':
                    if self.Objects.__contains__(e.name):
                        self.Objects[e.name](self.parent, e)

class Body(JLYObject):
    def __init__(self, parent):
        JLYObject.__init__(self, parent)
        self.actionListener = parent.actionListener
        self.theme = parent.theme
        self.background = '#cccccc'
        self.selected = None
        self.content = []

    def build(self, data):
        for e in data.elements:
            if e.dType == 'object':
                if self.Objects.__contains__(e.name):
                    self.Objects[e.name](self, e)

    def getFrame(self, **kws):
        return self.parent.frame

    def addContent(self, content):
        self.content.append(content)

    def focus(self, comp, foucused):
        if foucused:
            self.selected = comp

class Head(JLYObject):
    def __init__(self, parent):
        JLYObject.__init__(self, parent)

    def build(self, data):
        root = self.parent.root

        width = '600'; height='400';
        minw = 600; minh = 400;
        maxw = 600; maxh = 400
        for e in data.elements:
            if e.dType == 'field':
                if e.name == 'title':
                    root.title(e.data)
                if e.name == 'resizeable':
                    b = e.data == 'true'
                    root.resizable(width=b, height=b)
                if e.name == 'size':
                    s = e.data.split(',')
                    root.geometry('%sx%s' % (eval(s[0]), eval(s[1])))
                if e.name == 'width':
                    width = e.data
                    root.geometry('%sx%s' % (eval(width), eval(height)))
                if e.name == 'height':
                    height = e.data
                    root.geometry('%sx%s' % (eval(width), eval(height)))
                if e.name == 'minsize':
                    s = e.data.split(',')
                    root.minsize(eval(s[0]), eval(s[1]))
                if e.name == 'minwidth':
                    minw = int(e.data)
                    root.minsize(minw, minh)
                if e.name == 'minheight':
                    minh = int(e.data)
                    root.minsize(minw, minh)
                if e.name == 'maxsize':
                    s = e.data.split(',')
                    root.maxsize(eval(s[0]), eval(s[1]))
                if e.name == 'maxwidth':
                    maxw = eval(e.data)
                    root.minsize(maxw, maxh)
                if e.name == 'maxheight':
                    maxh = eval(e.data)
                    root.minsize(maxw, maxh)
                if e.name == 'background':
                    root.wait_visibility(root)
                    #root.wm_attributes("-alpha", 0.8)
                    self.parent.body.background = Color(self, e.data).get()
                    self.parent.frame['bg'] = Color(self, e.data).get()

class For(JLYObject):
    def __init__(self, parent, data):
        JLYObject.__init__(self, parent)

        if data.oneline:
            return
            #data.readLine()

        var = data.getP(0).replace(' ', '')
        bexp = data.getP(1).replace(' ', '')
        end = data.getP(2).replace(' ', '')

        v = var.split('=', 1)
        if len(v) > 1:
            self.vars[v[0]] = Int(self, v[1])
        else:
            self.vars[v[0]] = Int(self, '0')

        self.execute(v)

        while self.eval(bexp):
            for e in data.elements:
                if e.dType == 'object':
                    if self.Objects.__contains__(e.name):
                        self.Objects[e.name](parent, e)
            self.execute(end)
