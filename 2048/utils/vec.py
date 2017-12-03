
import numpy as np

class Vec():
    def __init__(self, *c):
        self.set(*c)

    def set(self, *c):
        if len(c) < 1: return
        while len(c) == 1 and isinstance(c[0], (list, tuple)):
            c = c[0]

        if isinstance(c[0], Vec): self.a = c[0].a
        else: self.a = np.array(c)

        self.a = self.a.astype(np.float)

    def dot(self, other):
        return self.a.dot(other.a)

    def norm(self):
        return np.linalg.norm(self.a)

    def normalize(self):
        return self / self.norm()

    def asTuple(self):
        return tuple(self.a)

    def floor(self):
        return self.a.astype(np.int)

    def __str__(self):
        return 'Vec' + str(self.a)

    def operator(self, other, func):
        new = Vec()
        if isinstance (other, (float, int)):
            new.a = func(self.a, other)
        elif isinstance(other, Vec):
            new.a = func(self.a, other.a)
        return new

    def __add__(self, other):
        return self.operator(other, lambda a,b: a + b)

    def __sub__(self, other):
        return self.operator(other, lambda a,b: a - b)

    def __mul__(self, other):
        return self.operator(other, lambda a,b: a * b)

    def __div__(self, other):
        return self.operator(other, lambda a,b: a / b)

    def __eq__(self, other):
        if not isinstance(other, Vec): return False
        return (self.a == other.a).all()

    def __ne__(self, other):
        if not isinstance(other, Vec): return True
        return (self.a != other.a).any()

    def __iter__(self):
        return iter(self.a)

    def __getitem__(self, index):
        return self.a[index]

    def __setitem__(self, index, value):
        self.a[index] = value

class IVec(Vec):
    def set(self, *c):
        if len(c) < 1: return
        while len(c) == 1 and isinstance(c[0], (list, tuple)):
            c = c[0]

        if isinstance(c[0], Vec): self.a = c[0].a
        else: self.a = np.array(c)

        self.a = self.a.astype(np.int)

class Vec2(Vec):

    def __init__(self, *c):
        self.set(*c)
        if len(self.a) == 0: self.set(0,0)
        if len(self.a) == 1: self.set(self.a, self.a)
