
# result: 209566
# Correct !

def tiles(w, l):
    return 4 * w**2 + 4 * w*l

maxT = 1000000
count = 0

t = []

w = 1; l = 1
s = tiles(w, l)
while s <= maxT:
    while s <= maxT:
        t.append(s)
        l += 1
        s = tiles(w, l)
    w += 1; l = 1
    s = tiles(w, l)

L = {}
for a in t:
    if L.__contains__(a):
        L[a] += 1
    else:
        L[a] = 1

N = {}
for k in L:
    if N.__contains__(L[k]):
        N[L[k]] += 1
    else:
        N[L[k]] = 1

print N[15]

result = 0
for i in range(10):
    if N.__contains__(i+1):
        result += N[i+1]
        print i+1
print result
