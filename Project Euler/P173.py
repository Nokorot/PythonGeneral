
# result: 1572729
# Correct !

def tiles(w, l):
    return 4 * w**2 + 4 * w*l

N = 100
count = 0

w = 1; l = 1
while tiles(w, l) <= N:
    count += 1
    l += 1
    while tiles(w, l) <= N:
        count += 1
        l += 1
    w += 1
    l = 1

print count
