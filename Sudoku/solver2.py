
silent = True

class Solver:
    def get(self, x, y):
        return self.Fields[x + y*9]

    def __init__(self, dim=(9,9), onSet=None):
        self.Fields = [Field(self, x, y) for y in range(dim[1]) for x in range(dim[0])]
        self.filld = 0
        self.DONE = False

        self.onSet = onSet if onSet else lambda f: None

    def SecondLevel(self):
        results = False
        for i in range(9):
            bolke = [self.get((i%3)*3 + j%3, (i/3)*3 + j/3) for j in range(9)]

            for n in range(1, 10):
                s = 0
                lf = None
                for f in bolke:
                    if type(f.possible) == int:
                        if f.possible == n:
                            s = 0
                            break
                    elif f.possible.__contains__(n):
                        lf = f
                        s += 1
                    if s > 1:
                        break
                if s == 1:
                    results = True
                    lf.set(n)
        return results

    def ThirdLevel(self):
        results = False
        for i in range(9):
            bolke = [self.get((i%3)*3 + j%3, (i/3)*3 + j/3) for j in range(9)]

            for n in range(1, 10):
                fs = []
                for f in bolke:
                    if type(f.possible) == int:
                        if f.possible == n:
                            f = []
                            break
                    elif f.possible.__contains__(n):
                        fs.append(f)
                if len(fs) == 2:
                    if fs[0].x == fs[1].x:
                        for j in range(9):
                            if [fs[0].y, fs[1].y].__contains__(j):
                                continue
                            ff = self.get(fs[0].x, j)
                            if type(ff.possible) != int and ff.possible.__contains__(n):
                                results = True
                                ff.remove(n)

                    if fs[0].y == fs[1].y:
                        for j in range(9):
                            if [fs[0].x, fs[1].x].__contains__(j):
                                continue
                            ff = self.get(j, fs[0].y)
                            if type(ff.possible) != int and ff.possible.__contains__(n):
                                results = True
                                ff.remove(n)

                if len(fs) == 3:
                    if fs[0].x == fs[1].x and fs[1].x == fs[2].x:
                        for j in range(9):
                            if [fs[0].y, fs[1].y, fs[2].y].__contains__(j):
                                continue
                            ff = self.get(fs[0].x, j)
                            if type(ff.possible) != int and ff.possible.__contains__(n):
                                results = True
                                ff.remove(n)

                    if fs[0].y == fs[1].y and fs[1].y == fs[2].y:
                        for j in range(9):
                            if [fs[0].x, fs[1].x, fs[2].x].__contains__(j):
                                continue
                            ff = self.get(j, fs[0].y)
                            if type(ff.possible) != int and ff.possible.__contains__(n):
                                results = True
                                ff.remove(n)


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

    def useMethods(self, methodLimit=None):
        c = 0
        if not methodLimit: methodLimit = 5
        while not self.DONE:
            giveUp = True

            if methodLimit > 1 and self.SecondLevel():
                if not silent: print 'Second level'
                giveUp = False

            if methodLimit > 2 and giveUp and self.ThirdLevel():
                if not silent: print 'Third level'
                giveUp = False

            if methodLimit > 3 and giveUp and self.FourthLevel():
                if not silent: print 'Fourth level'
                giveUp = False

            if methodLimit > 4 and giveUp and self.FifthLevel():
                if not silent: print 'Fifth level'
                giveUp = False

            if giveUp:
                if not silent: print 'Gives Up'
                break

class Field:
    def __init__(self, solver, x, y):
        self.possible = [i+1 for i in range(9)]
        self.solver = solver
        self.index = x + y * 9
        self.x = x
        self.y = y
        self.wrong = False

    def set(self, value):
        if type(self.possible) == int:
            if value != self.possible:
                self.wrong = True
            return
        if type(value) == list:
            for v in self.possible[:]:
                if not value.__contains__(v):
                    self.remove(v)
            return

        self.possible = value
        self.solver.filld += 1
        self.solver.DONE = self.solver.filld >= 81

        self.solver.onSet(self)

        for i in range(9):
            self.solver.Fields[self.x/3*3 + i%3 + (self.y/3*3 + i/3)*9].remove(value, self)
            if i != self.x: self.solver.Fields[i + self.y*9].remove(value)
            if i != self.y: self.solver.Fields[self.x + i*9].remove(value)

    def open(self):
        self.possible = [i+1 for i in range(9)]
        self.solver.filld -= 1
        self.solver.DONE = self.solver.filld >= 81

    def get(self):
        if type(self.possible) == int:
            return self.possible
        return None

    def remove(self, value, other=None):
        if self == other:
            return
        if type(self.possible) == int:
            if value == self.possible:
                self.wrong = True
            return
        if self.possible.__contains__(value):
            self.possible.remove(value)
        if len(self.possible) == 1:
            self.set(self.possible[0])

    def value(self):
        if self.get():
            return self.get()
        else:
            return self.possible

def solve(values, dim=(9,9), methodLimit=None):
    solver = Solver(dim)

    for f, v in zip(solver.Fields, values):
        try: v = int(v)
        except ValueError: continue
        f.set(v)

    solver.useMethods(methodLimit)

    i = 0
    for f in solver.Fields:
        if f.wrong:
            values[i] = '*'+str(f.get())+'*'
        elif f.get():
            values[i] = str(f.get())
        else:
            values[i] = str(f.possible)
        i += 1
    return solver.DONE
