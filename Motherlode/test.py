
w = 5; h = 5;

def index(x, y, i, dir):
    if (dir == 'Left'):
        if (x - i < 0): return -1
        return (x - i) + y * w
    if (dir == 'Right'):
        if (w-1 - x + i >= w): return -1
        return (w-1 - x + i) + y * w
    if (dir == 'Down'):
        if (h-1 - y + i >= h): return -1
        return x + (h-1 - y + i) * w
    if (dir == 'Up'):
        if (y - i < 0): return -1;
        return x + (y - i) * w

i = index(1, 0, 1, 'Left')

if i < 0:
    print -1
else:
    print i%w, i/w
