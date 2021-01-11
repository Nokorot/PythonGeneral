#!/usr/bin/python

if False:
    def f(x):
        return x**2

class JLYObjectData:
    def __init__(self, name, props, data):
        self.name = name
        self.props = props

        if type(data) == str:
            self.data = data
        elif type(data) == tuple:
            self.fields = data[0]
            self.objects = data[1]
        else:
            print 'A JLYObject does not take data as ' + str(type(data)) + ', only str and tuple (len == 2)'

        self.oneline = type(data) == str

        if self.oneline:
            def readLine(self):
                reader = JLYReaderFromString(self.data)
                reader.read()
                self.objects = reader.objects
                self.fields = reader.fields

            self.readLine = lambda: readLine(self)


    def show(self, t=0):
        s = '    '*t + self.name + str(self.props) + ':'
        t += 1

        if self.oneline:
            s += '  ' + self.data

        print s

        if not self.oneline:
            for f in self.fields:
                if type(f) == tuple:
                    print '    '*t + 'tuple - ' + str(f)
                else:
                    f.show(t)
            for o in self.objects:
                o.show(t)

    def getO(self, name):
        ''' returns a list of objects with the name 'name' '''
        result = []
        for o in self.objects:
            if o.name == name:
                result.append(o)
        return result

    def getF(self, name):
        ''' returns a list of fields with the name 'name' '''
        result = []
        for f in self.fields:
            if f.name == name:
                result.append(f)
        return result

class JLYFieldData:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def show(self, t=0):
        s = '    '*t + self.name + ':'
        t += 1

        if type(self.data) == str:
            s += '  ' + self.data

        print s

        if type(self.data) == tuple:
            for f in self.data[0]:
                f.show(t)
            for o in self.data[1]:
                o.show(t)

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
        self.fields = []
        self.objects = []
        self.line = 0

    def show(self):
        for f in self.fields:
            f.show(t)
        for o in self.objects:
            o.show()

    def getO(self, name):
        ''' returns a list of objects with the name 'name' '''
        result = []
        for o in self.objects:
            if o.name == name:
                result.append(o)
        return result

    def getF(self, name):
        ''' returns a list of fields with the name 'name' '''
        result = []
        for f in self.fields:
            if f.name == name:
                result.append(f)
        return result

    def next(self):
        self.index += 1
        if self.index >= len(self.data):
            return False
        c = self.data[self.index]
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
        props = {}
        while self.index < len(self.data):
            c = self.next()
            if not c: break
            if ['\t', '\n', ' '].__contains__(c): continue

            if c == ';' or c == '>':
                a = prop.split(':')
                if len(a) == 1:
                    props[i] = prop
                    i += 1
                elif len(a) == 2:
                    props[a[0]] = a[1]
                else:
                    pass #raise 'Syntax Error - %i' % self.line
                prop = ''
                if c == '>': break
                continue
            prop += c

        return props

    def readFild(self, end=['\n', ';']):
        self.index -= 1
        field = ''
        while self.index < len(self.data):
            c = self.next()
            if not c: return None
            if ['\t', ' '].__contains__(c): continue
            if end.__contains__(c): break
            if c == '}':
                self.index -= 1
                break
            if c == '{':
                data = self.readData()
                A = {}
                for f in data[0]:
                    A[f.name] = f.data
                return JLYFieldData(field, A)
            field += c

        f = field.split(':')
        if len(f) < 2:
            return None
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
            if c == '\t' or c == ' ': continue
            if c == '{':
                data = self.readData()
                break
            data += c

        return JLYObjectData(name, props, data)

    def readData(self):
        filds = []
        objects = []
        while self.index < len(self.data):
            c = self.next()
            if not c: break
            if ['\t', '\n', ' '].__contains__(c): continue
            if c == '{':
                o, f = self.readData()
                objects.append(o)
                filds.append(f)
            if c == '}': self.next(); break
            if c == '<':
                objects.append(self.readObject())
            f = self.readFild()
            if not f: continue
            filds.append(f)
        return filds, objects

    def read(self):
        self.index = -1
        self.fields, self.objects = self.readData()

if __name__ == '__main__':
    #jly = open('MainMenu.jly', 'r').read()

    reader = JLYReader('MainMenu.jly')
    reader.read()
    reader.show()
