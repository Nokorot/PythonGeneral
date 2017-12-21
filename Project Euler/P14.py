
'''-- Problem 14

mfac = (map fac [0..] !!)
    where fac 0 = 1
          fac n = trace (show n) (n* mfac (n-1))

collatzS 1 = 1
collatzS n
    | mod n 2 == 0 = 1+ collatzS (div n 2)
    | otherwise    = 1+ collatzS (3*n+1)

mcollatzS = (map (\n -> func n) [0..] !!)
    where func 0 = 0
          func 1 = 1
          func n = if (mod n 2 == 0)
                   then 1+ mcollatzS (div n 2)
                   else 1+ mcollatzS (3*n+1)'''

import numpy as np

N = np.zeros(1000000, int)
N[1] = 1
def collatz(n):
    if n <= 0: return 0
    if n < len(N) and N[n] != 0:
        return N[n]
    if n % 2 == 0:
        m = 1+collatz(n / 2)
    else:
        m = 1+collatz(3*n+1)
    if n < len(N):
        N[n] = m
    return m

M = 0
for n in range(1000000):
    m = collatz(n)
    if m > M:
        M = m
        print n, m
