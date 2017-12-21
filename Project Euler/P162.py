

def choose(a, b):
    if a == 0:
        return 1
    return float(b) / a * choose(a-1, b-1)

def fact(a):
    out = 1
    for i in range(1,a+1):
        out *= i
    return out

def npr(a, b):
    out = 1
    for i in range(a):
        out *= (b-i)
    return out



def A(a, b):
    return 15 * npr(a-1, 15) * (16-a)**(16-a)

    #return int(choose(a, 16)) * 3**(a-3)*fact(3) * (16-3)**(16-3)


print A(3, 0)
print 15*15*14 * (16-3)**(16-3)
