import math
#import numpy

class matrix(object):
    def nCr(n,r):
        f = math.factorial
        return f(n) / f(r) / f(n-r)

    def __init__(self, n, q):
        self.n = n
        self.q = q
        f = math.factorial
        size = f(n) / f(q) / f(n-q)
        self.r = size
        self.c = size
        self.m = []

    def toBaseN(n,t):
        sum = 0
        p = n-1
        for i in t:
            sum += pow(i,p)
            i = i +1
            p = p +1
        return sum

    def fromBaseN(n,q,d):
        p=n-1
        l = []
        for i in range(0,q-1):
            l[i] = divmod(d,pow(n,q))
            d = int(d/pow(n,q))
        l.reverse()
        return tuple(list)

 #   def initMatrix(self):












