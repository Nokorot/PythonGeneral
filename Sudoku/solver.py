
import copy

silent = True

class Grid:
    def __init__(self, dim=(3,3)):
        self.w, self.h = dim
        self.vrange = dim[0] * dim[1]
        self.cells = [Cell(self, x, y, self.vrange) for y in range(self.vrange) for x in range(self.vrange)]
        self.filled = 0
        self.IS_DONE = False
        self.IS_FALSE = False

    def get(self, x, y):
        return self.cells[x + y*self.vrange]

    def set(self, x, y, value):
        self.cells[x + y*self.vrange].set(value);

    def reduce(self, x, y, value):
        self.cells[x + y*self.vrange].reduce(value)

    def blocks(self):
        for i in range(self.w * self.h):
            yield self.getBlock(i%self.h, i/self.h)

    def lines(self):
        vr = self.vrange
        for i in range(vr):
            yield self.cells[i*vr: (i+1)*vr]
            yield self.cells[i::vr]

    def getBlock(self, i, j):
        return [self.get(i*self.w + k%self.w, j*self.h + k/self.w) for k in range(self.vrange)]

    def __str__(self):
        vr = self.vrange
        return '\n'.join([' '.join(map(str, self.cells[i*vr : (i+1)*vr])) for i in range(vr)])

class Cell:
    def __init__(self, grid, x, y, vrange):
        self.grid, self.x, self.y, self.vrange = grid, x, y, vrange
        self.values = [i+1 for i in range(vrange)]
        self.IS_FALSE = False

    def makeFalse(self):
        self.IS_FALSE = True
        self.grid.IS_FALSE = True

    def set(self, value):
        self.values = value
        if type(value) == int:
            self.grid.filled += 1
        if self.grid.filled == len(self.grid.cells):
            self.grid.IS_DONE = True

        w,h,vr = self.grid.w, self.grid.h, self.vrange
        for i in range(vr):
            xa,ya = self.x/w*w + i%w, self.y/h*h + i/w
            if xa != self.x and ya != self.y:
                self.grid.reduce(xa, ya, value)
                if self.IS_FALSE:
                    return
        for i in range(vr):
            if i != self.x: self.grid.reduce(i, self.y, value)
            if i != self.y: self.grid.reduce(self.x, i, value)
            if self.IS_FALSE:
                return

    def reduce(self, value):
        if type(self.values) == int:
            if self.values == value:
                self.makeFalse()
            return
        if type(self.values) == list and not self.values.__contains__(value):
            return
        self.values.remove(value)
        if len(self.values) == 0:
            self.makeFalse()
        elif len(self.values) == 1:
            self.set(self.values[0])

    def __str__(self):
        if self.IS_FALSE:
            return '*%s*' % str(self.values)
        return str(self.values)

class Solver:
    def __init__(self, values, dim=(3,3)):
        self.values = values
        self.grid = Grid(dim)
        self.w, self.h = dim
        self.vrange = dim[0] * dim[1]
        self.forceFrames = []
        self.solutions = []

        for c, v in zip(self.grid.cells, values):
            try: v = int(v)
            except ValueError: continue
            c.set(v)

    def solve(self, methodLimit=None):
        self.useMethods(3)#methodLimit)

        if len(self.solutions) > 0:
            for i in range(len(self.solutions[0].cells)):
                self.values[i] = str(self.solutions[0].cells[i])
            return self.solutions[0].IS_DONE

    def SecondLevel(self):
        results = False
        def checkUniqness(block, n):
            lc = None
            for c in block:
                if c.values == n:
                    return
                elif type(c.values) == list and c.values.__contains__(n):
                    if lc != None:
                        return
                    lc = c
            if lc != None:
                lc.set(n)
                #print 'L2:', (lc.x, lc.y), n
                return True

        '''for block in self.grid.blocks():
            for n in range(1, self.vrange+1):
                checkUniqness(block, n)'''
        for line in self.grid.lines():
            for n in range(1, self.vrange+1):
                if checkUniqness(line, n):
                    results = True
                if self.grid.IS_FALSE:
                    return False
        return results

    def ThirdLevel(self):
        results = False
        def checkAlignment(block, n):
            cs = []
            for c in block:
                if c.values == n:
                    return
                elif type(c.values) == list and c.values.__contains__(n):
                    cs.append(c)
            if len(cs) == 1:
                cs[0].set(n)
                #print 'L2.5:', (cs[0].x, cs[0].y), n
                return True
            elif len(cs) > 1:
                if all(c.x == cs[0].x for c in cs):
                    for j in range(self.vrange):
                        if any(c.y == j for c in cs):
                            continue
                        ff = self.grid.get(cs[0].x, j)
                        if type(ff.values) == list and ff.values.__contains__(n):
                            results = True
                            ff.reduce(n)
                            #print 'L3_r:', (ff.x, ff.y), n
                elif all(c.y == cs[0].y for c in cs[:]):
                    for j in range(self.vrange):
                        if any(c.x == j for c in cs):
                            continue
                        ff = self.grid.get(j, cs[0].y)
                        if type(ff.values) == list and ff.values.__contains__(n):
                            results = True
                            ff.reduce(n)
                            #print 'L3_c:', (ff.x, ff.y), n

        for block in self.grid.blocks():
            for n in range(self.vrange):
                if checkAlignment(block, n):
                    results = True
                if self.grid.IS_FALSE:
                    return False
        return results

    def FourthLevel(self):
        results = False
        for j in range(1, 9+1):
            for y in range(9):
                containing = []
                for x in range(9):
                    f = self.get(x, y)
                    if type(f.possible) == int:
                        if f.get() == j:
                            break
                        else:
                            continue
                    if f.possible.__contains__(j):
                        containing.append(f)
                if len(containing) == 1:
                    containing[0].set(j)
                    results = True

            for x in range(9):
                containing = []
                for y in range(9):
                    f = self.get(x, y)
                    if f.get():
                        if f.get() == j:
                            break
                        else:
                            continue
                    if f.possible.__contains__(j):
                        containing.append(f)
                if len(containing) == 1:
                    containing[0].set(j)
                    results = True
        return results

    def FifthLevel(self):
        results = False

        return False

        # rows
        for y in range(9):
            pos = {}
            for j in range(1, 9+1):
                jpos = []
                for x in range(9):
                    f = self.get(x,y)
                    if type(f.possible) == int:
                        continue
                    if f.possible.__contains__(j):
                        jpos.append(x)
                jpos = tuple(jpos)
                if pos.__contains__(jpos):
                    pos[jpos].append(j)
                else:
                    pos[jpos] = [j]

            for jpos in pos:
                if len(jpos) == len(pos[jpos]):
                    for i in jpos:
                        if self.get(i, y).possible != pos[jpos]:
                            self.get(i, y).set(pos[jpos])
                            results = True
                            if not silent: print 'y', y, jpos, pos[jpos]

        # colomns
        for x in range(9):
            pos = {}
            for j in range(1, 9+1):
                jpos = []
                for y in range(9):
                    f = self.get(x,y)
                    if type(f.possible) == int:
                        continue
                    if f.possible.__contains__(j):
                        jpos.append(y)
                jpos = tuple(jpos)
                if pos.__contains__(jpos):
                    pos[jpos].append(j)
                else:
                    pos[jpos] = [j]

            for jpos in pos:
                if len(jpos) == len(pos[jpos]):
                    for i in jpos:
                        if self.get(x, i).possible != pos[jpos]:
                            self.get(x, i).set(pos[jpos])
                            results = True
                            if not silent: print 'x', x, jpos, pos[jpos]


        return results

    def ForceLevel(self):
        gridcp = copy.deepcopy(self.grid)

        for c in self.grid.cells:
            if type(c.values) == list:
                if not silent: print "ForceLevel:", c.x, c.y
                self.forceFrames.append((gridcp, c.x, c.y, c.values[0]))
                c.set(c.values[0])
                return

    def popForceFrame(self):
        if not silent: print 'popForceFrame', len(self.forceFrames)
        frame = self.forceFrames.pop()
        self.grid = frame[0]
        self.grid.reduce(frame[1], frame[2], frame[3])

    def useMethods(self, methodLimit=None):
        if not methodLimit: methodLimit = 5
        while True:
            giveUp = True

            if methodLimit > 1 and self.SecondLevel():
                if not silent: print 'Second level'
                giveUp = False

            if methodLimit > 2 and giveUp and self.ThirdLevel():
                if not silent: print 'Third level'
                giveUp = False

            '''if methodLimit > 3 and giveUp and self.FourthLevel():
                if not silent: print 'Fourth level'
                giveUp = False

            if methodLimit > 4 and giveUp and self.FifthLevel():
                if not silent: print 'Fifth level'
                giveUp = False
            '''

            if giveUp and not self.grid.IS_FALSE:
                self.ForceLevel()

            if self.grid.IS_FALSE:
                if len(self.forceFrames) > 0:
                    self.popForceFrame()
                else:
                    break
            elif self.grid.IS_DONE:
                self.solutions.append(self.grid)
                if len(self.forceFrames) > 0:
                    self.popForceFrame()
                else:
                    break

def solve(values, dim=(3,3), methodLimit=None):
    return Solver(values, dim).solve(methodLimit)

if __name__ == '__main__':
    g = Grid((2,3))
    g.set(0,0, 1)
    g.set(1,1, 2)
    g.set(2,2, 3)
    g.set(3,3, 4)
    g.set(4,4, 5)
    g.set(5,5, 6)
    print g
