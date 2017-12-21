
import numpy as np

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

import numpy
def primesfrom2to(n):
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = numpy.ones(n/3 + (n%6==2), dtype=numpy.bool)
    for i in xrange(1,int(n**0.5)/3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k/3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)/3::2*k] = False
    return numpy.r_[2,3,((3*numpy.nonzero(sieve)[0][1:]+1)|1)]

class primes:
    def __init__(self, n=1000, add=1000):
        self.n = n
        self.add = add

        sieve = np.ones(n/2, dtype=np.bool)
        for i in xrange(3,int(n**0.5)+1,2):
            if sieve[i/2]:
                sieve[i*i/2::i] = False
        self.primes = np.r_[2, (2*np.nonzero(sieve)[0][1::]+1)]

    def genprimes(self, to=None):
        n, m = self.n, self.add
        if to != None:
            m = max(m, to-self.n + 1)
            while to > self.primes[-1]**2-1:
                self.genprimes(self.primes[-1]**2-1)

        sieve = np.ones(m, dtype=np.bool)
        for i in self.primes:
            if i**2 > n+m:
                break
            sieve[(i-(n%i))::i] = False
        self.primes = np.r_[self.primes, np.nonzero(sieve)[0][1::]+n]
        self.n += m

    def isPrime(self, num):
        if num >= self.n:
            self.genprimes(num)
        return p.primes.__contains__(num)

    def __getintem__(self, i):
        while i > len(self.data):
            self.genprimes()
        return self.data[i+1]

def combinations(length, set):
    a = len(set)
    for n in range(len(set)**length):
        yield [set[(n / a**i) % a] for i in range(length)]

p = primes()

from math import log10
def isTPrime(a):
    n = int(log10(a))
    if not p.isPrime(a):
        return False
    b = a
    while n > 0:
        a = int(a / 10)
        b = int(b % 10**n)
        if not p.isPrime(a) or not p.isPrime(b):
            return False
        n -= 1
    return True

j = 0
for i in range(11, 10000):
    if isTPrime(i):
        j += 1
        print i
print 'result: ' + str(j)
