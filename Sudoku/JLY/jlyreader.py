#!/usr/bin/python

import sys

if False:
    def f(x):
        return x**2

class JLYDataelement:
    def __init__(self, dType):
        self.dType = dType

    def __str__(self):
        return self.dType

class JLYStringData(JLYDataelement):
    def __init__(self, data):
        JLYDataelement.__init__(self, 'string')
        self.data = data

class JLYObjectData(JLYDataelement):
    def __init__(self, name, props, data):
        JLYDataelement.__init__(self, 'object')
        self.name = name
        self.props = props

        if type(data) == str:
            self.data = data
        elif type(data) == list:
            self.elements = data
        else:
            print 'A JLYObject does not take data as ' + str(type(data)) + ', only str and list'


        self.oneline = type(data) == str

        if self.oneline:
            def readLine(self):
                reader = JLYReaderFromString(self.data)
                reader.read()
                self.objects = reader.objects
                self.fields = reader.fields

            self.readLine = lambda: readLine(self)

    def str(self, t=0):
        out = '    '*t + self.name + str(self.props) + ':'
        t += 1

        if self.oneline:
            out += '  ' + self.data

        out += '\n'

        if not self.oneline:
            for e in self.elements:
                out += e.str(t)

        return out

    def __str__(self):
        return self.str();

    def getP(self, key):
        for p in self.props:
            if p.name == key:
                return p.data

    '''def getO(self, name):
         returns a list of objects with the name 'name'
        result = []
        for o in self.objects:
            if o.name == name:
                result.append(o)
        return result

    def getF(self, name):
         returns a list of fields with the name 'name'
        result = []
        for f in self.fields:
            if f.name == name:
                result.append(f)
        return result'''

class JLYFieldData(JLYDataelement):
    def __init__(self, name, data):
        JLYDataelement.__init__(self, 'field')
        self.name = name

        if type(data) == str:
            while len(data) > 0 and data[0] == ' ':
                data = data[1:]
            self.data = data
        elif type(data) == list:
            self.elements = data
        else:
            print 'A JLYObject does not take data as ' + str(type(data)) + ', only str and list'


        self.oneline = type(data) == str

        if self.oneline:
            def readLine(self):
                reader = JLYReaderFromString(self.data)
                reader.read()
                self.objects = reader.objects
                self.fields = reader.fields

            self.readLine = lambda: readLine(self)

    def str(self, t=0):
        out = '    '*t + str(self.name) + ':'
        t += 1

        if self.oneline:
            out += '  ' + self.data

        out += '\n'

        if not self.oneline:
            for e in self.elements:
                out += e.str(t)

        return out

    def __str__(self):
        return self.str()

def JLYReaderFromString(string):
    reader = JLYReader('')
    reader.data = string
    return reader

class JLYReader:
    def __init__(self, filename):
        self.data = None
        try:
            self.data = open(filename, 'r').read()
        except:
            print 'No such file or directory: ' + filename

        self.elements = []
        self.line = 0

    def show(self):
        print 'showing'
        for e in self.elements:
            print e
        '''for f in self.fields:
            f.show(t)
        for o in self.objects:
            o.show()'''

    '''def getO(self, name):
        #returns a list of objects with the name 'name'
        result = []
        for o in self.objects:
            if o.name == name:
                result.append(o)
        return result

    def getF(self, name):
        #returns a list of fields with the name 'name'
        result = []
        for f in self.fields:
            if f.name == name:
                result.append(f)
        return result'''

    def get(self, key):
        A = []
        for e in self.elements:
            if e.name == key:
                A.append(e)
        if len(A) == 0:
            return None
        if len(A) == 1:
            return A[0]
        return A

    def next(self):
        self.index += 1
        if self.index >= len(self.data):
            return False
        self.c = c = self.data[self.index]
        if c == '\t': c = ' '
        if len(self.data) > self.index + 1:
            while c == ' ' and self.data[self.index + 1] == ' ':
                self.index += 1
                c = self.data[self.index]
                if c == '\t': c = ' '
            if c == '/' and self.data[self.index + 1] == '/':
                while c != '\n':
                    self.index += 1
                    c = self.data[self.index]
        if c == '\n':
            self.line += 1
        return c

    def readProps(self):
        i = 0
        prop = ''
        props = []
        while self.next():
            if ['\t', '\n'].__contains__(self.c): continue

            prop = self.readFild(end=[',', '>'])
            if type(prop) == str:
                props.append(JLYFieldData(i, prop))
                i += 1
            else:
                props.append(prop)

            if self.c == '>': break
            '''if [';', '>'].__contains__(c):
                a = prop.split(':')
                if len(a) == 1:
                    props[i] = prop[1:] if prop[0] == ' ' else prop
                    i += 1
                elif len(a) == 2:
                    props[a[0].replace(' ', '')] = a[1][1:] if a[1][0] == ' ' else a[1]
                else:
                    pass #raise 'Syntax Error - %i' % self.line
                prop = ''
                if c == '>': break
                continue
            prop += c'''

        return props

    def readFild(self, end=['\n', ';']):
        self.index -= 1
        field = ''
        while self.index < len(self.data):
            c = self.next()
            if not c: return None
            if ['\t'].__contains__(c): continue
            if end.__contains__(c): break
            if c == '}':
                self.index -= 1
                break
            if c == '{':
                data = self.readData()
                '''A = {}
                for e in data:
                    print e
                for f in data[0]:
                    A[f.name] = f.data'''
                return JLYFieldData(field, data)
            if c == '"':
                field = self.readString()
            field += c

        while len(field) > 0 and field[0] == ' ':
            field = field[1:]

        f = field.split(':')
        if len(f) < 2:
            return f[0]
        return JLYFieldData(f[0], f[1])

    def readObject(self):
        name = ''
        data = ''
        props = {}
        while self.index < len(self.data):
            c = self.next()
            if not c: break
            if ['\t', '\n'].__contains__(c): continue
            if c == '>': break
            if c == ',': props = self.readProps(); break
            name += c

        while self.index < len(self.data):
            c = self.next()
            if not c: break
            if c == '\n': break
            if c == '\t': continue
            if c == '"':
                data = self.readString()
            if c == '{':
                data = self.readData()
                break
            data += c

        return JLYObjectData(name, props, data)

    def readData(self):
        elements = []
        while self.index < len(self.data):
            c = self.next()
            if not c: break
            if ['\t', '\n', ' '].__contains__(c): continue
            if c == '{':
                elements.append(self.readData())
            if c == '}': self.next(); break
            if c == '<':
                elements.append(self.readObject())
            f = self.readFild()
            if not f: continue
            elements.append(f)
        return elements

    def readString(self):
        index = self.index
        while self.next():
            if self.c == '"': break
        return self.data[index:self.index]

    def read(self):
        self.index = -1
        self.elements = self.readData()


if __name__ == '__main__':
    #jly = open('MainMenu.jly', 'r').read()

    reader = JLYReader('MainMenu.jly')
    reader.read()
    reader.show()
