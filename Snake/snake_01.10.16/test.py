from math import sqrt

class vec2():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        if(isinstance(other, vec2)):
            return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if(isinstance(other, vec2)):
            return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if(isinstance(other, vec2)):
            return vec2(self.x * other.x, self.y * other.y)
        elif(type(other) == float or type(other) == int):
            return vec2(self.x * other, self.y * other)

    def __div__(self, other):
        if(isinstance(other, vec2)):
            return vec2(self.x / other.x, self.y / other.y)
        elif(type(other) == float or type(other) == int):
            return vec2(self.x / other, self.y / other)

    def __mod__(self, other):
        if(isinstance(other, vec2)):
            return vec2(self.x % other.x, self.y % other.y)
        elif(type(other) == float or type(other) == int):
            return vec2(self.x % other, self.y % other)

    def __iadd__(self, other):
        self = self + other
        return self

    def __isub__(self, other):
        self = self - other
        return self

    def __imul__(self, other):
         self = self * other
         return self

    def __idiv__(self, other):
        self = self / other
        return self

    def __imod__(self, other):
        self = self % other
        return self

    def __str__(self):
        return '[%g, %g]' % (self.x, self.y)

    def asTuple(self):
        return (self.x, self.y)
