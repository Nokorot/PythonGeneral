from re import split

class Reader():
    def __init__(self, filename):
        inp = open(filename, 'r')
        self.index = -1
        self.lines = inp.readlines()

    def next(self):
        self.index += 1
        if not (self.index < len(self.lines)):
            return False, None
        l = self.lines[self.index][:-2]
        while (self.index+1 < len(self.lines) and self.lines[self.index+1][0] == ' '):
            self.index += 1
            l += self.lines[self.index][1:-1][:-2]
        return split('[:]', l, 1)

class ICSElement():
    def __init__(self):
        self.data = {}

    def read(self, reader): # TODO: check if the end, actualy ends this element
        while True:
            a,b = reader.next()
            if (not a) or a == 'END':
                return self
            elif a == 'BEGIN':
                if not self.data.__contains__(b):
                    self.data[b] = []
                self.data[b].append(ICSElement().read(reader))
            else:
                self.data[a] = b

    def assamble(self, other, overide=True):
        for k in other.data:
            do = other.data[k]
            if type(do) == list:
                if not self.data.__contains__(k):
                    self.data[k] = []
                self.data[k] += do
            elif overide:
                    self.data[k] = do

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __str__(self):
        return self.string()

    def string(self, t=0):
        indent = '    '
        result = ""
        for k in self.data:
            d = self.data[k]
            if isinstance(d, ICSElement):
                result += indent*t + k + '\n'
                result += d.string(t+1)
            elif type(d) == list:
                for e in d:
                    result += indent*t+k+'\n'
                    result += e.string(t+1)
            else:
                result += indent*t+k+"  "+d+'\n'
        return result

    def writeElement(self, f):
        for a in self.data:
            b = self[a]
            if(type(b) == list):
                for e in b:
                    f.write('BEGIN:' + a + '\n')
                    e.writeElement(f)
                    f.write('END:' + a + '\n')
            else:
                f.write(a + ':' + b + '\n')


class ICSData(ICSElement):

    def __init__(self, **kws):
        ICSElement.__init__(self)
        for kw in kws:
            if kw == 'file':
                self.loadFile(kws['file'])

    def calendar(self, index=0):
        return Calender(self["VCALENDAR"][0])

    def assamble(self, other):
        for k in other.data:
            if self.data.__contains__(k):
                self[k][0].assamble(other[k][0])
            else:
                self[k] = other[k]

    def loadFile(self, filename):
        reader = Reader(filename)
        self.data = ICSElement().read(reader).data
        return self

    def writeFile(self, filename):
        f = open(filename, 'w')
        self.writeElement(f)

class Calender(ICSElement):
    def __init__(self, element):
        assert isinstance(element, ICSElement)
        self.data = element.data

    def removeE(self, func):
        self['VEVENT'] = [e for e in self['VEVENT'] if not func(Event(e))]

    def events(self):
        return [Event(e) for e in self['VEVENT']]

class Event(ICSElement):
    def __init__(self, event):
        assert isinstance(event, ICSElement)
        self.data = event.data

    # TODO: make a time class
    def Start(self):
        return self['DTSTART'].replace('T', '').replace('Z', '')

    def End(self):
        return self['DTSTART'].replace('T', '').replace('Z', '')

    def UID(self):
        return self['UID']

    def Created(self):
        return self['CREADTED']

    def LastModified(self):
        return self['LAST-MODIFIED']

    def Location(self):
        return self['LOCATION']

    def Sequence(self):
        return self['SEQUENCE']

    def Status(self):
        return self['STATUS']

    def Summary(self):
        return self['SUMMARY']

    def Transp(self):
        return self['TRANSP']

    def Description(self):
        return self['DESCRIPTION']

def func(e):
    return int(e.Start()) < 20170101000000

#def hapendsBefore(time):
if __name__ == "__main__":
    ICS = ICSData(file="file.ics")
    cal = ICS.calendar()
    cal.removeE(func)

    ICS.writeFile("out2.ics")
#print cal
