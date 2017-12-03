
from random import randint

def fromBounds(bounds):
    if [float, int].__contains__(type(bounds)) \
        or len(bounds) == 1:
        x = y = 0
        width = height = bounds[0]
    elif len(bounds) == 2:
        x = y = 0
        height = bounds[1]
        width = bounds[0]
    elif len(bounds) == 4:
        x = bounds[0]
        y = bounds[1]
        width = bounds[2]
        height = bounds[3]
    else:
        print 'Iligele bounds \'%g\'' % bounds
        x = y = width = height = None
    return x, y, width, height

def mod2(v, m):
    if(type(m) == tuple and len(m) > 1):
        return v[0] % m[0], v[1] % m[1]
    else:
        return v[0] % m, v[1] % m

def add2(v0, v1):
    return v0[0] + v1[0], v0[1] + v1[1]

def sub2(v0, v1):
    return v0[0] - v1[0], v0[1] - v1[1]

def scale2(v, s):
    if(type(s) == tuple and len(s) > 1):
        return v[0] * s[0], v[1] * s[1]
    else:
        return v[0] * s, v[1] * s

def scale3(v, s):
    if(type(s) == tuple and len(s) > 2):
        return v[0] * s[0], v[1] * s[1], v[2] * s[2]
    else:
        return v[0] * s, v[1] * s, v[2] * s

def clamp(V, Vmin, Vmax):
    return max(min(V, Vmax), Vmin)


def sgn(v):
    if v > 0: return 1
    if v == 0: return 0
    return -1

def sum(A, i0=0, i1=-1):
    s = 0.
    if (i1 < i0):
        for e in A:
            s += e
    else:
        for i in range(i0, i1):
            s += A[i]
    return s
