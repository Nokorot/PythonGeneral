
class LineReader():
    def __init__(self, infile):
        self.infile = infile
        self.lines = []
        self.linecount = 0
        self.line = None
        self.index = -1

    def next(self):
        self.index += 1
        if self.index < self.linecount:
            self.line = self.lines[self.index]
            return self.line
        return False

    def empty(self):
        if self.line == None:
            return True
        if len (self.line.replace(' ', '') ) < 1:
            return True
        return False

    def load(self):
        with open(self.infile) as infile:
            self.lines = [l.strip() for l in infile]
            self.linecount = len(self.lines)
        return self.read()

    def read(self):
        def readElemet():
            content = {}
            while self.next():
                if self.empty(): continue

                A = self.line.split(':')
                a,b = A[0], A[1]

                if (not a) or a == 'END': return content
                elif a == 'BEGIN':
                    if not content.__contains__(b): content[b] = []
                    A[b].append(readElement(b))
                else: A[a] = b

        return readElemet()

class CharReader():
    def __init__(self, infile):
        self.infile = infile
        self.data = []
        self.datasize = 0
        self.curentline = 0
        self.index = -1
        self.char = ''

    def next(self, step=1):
        if step > 1: self.next(step-1)
        if self.char == '\n': self.curentline += 1
        self.index += 1
        if self.index < len(self.data):
            self.char = self.data[self.index]
            return self.char
        self.char = ''
        return False

    def coming(self, string):
        for i in range(len(string)):
            print i
            if self.data[self.index+i] != string[i]:
                return False
        return True

    def goto(self, string, past=False):
        while not self.coming(string):
            if not self.next(): return False
        if past and not self.next(len(string)): return False
        return True

    def load(self):
        with open(self.infile) as infile:
            self.data = infile.read()
            self.datasize = len(self.data)
        return self.read()

    def read(self):
        out = ''
        while self.next():
            if self.coming('//'):
                print self.char
                if not self.goto('\n'): break
            if self.coming('/*'):
                if not self.goto('*/', True): break
            out += self.char

        return out
