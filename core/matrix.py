import math
import numpy
from numpy import linalg as LA

class matrix(object):
    def nCr(n,r):
        f = math.factorial
        return f(n) / f(r) / f(n-r)

    def __init__(self, n, q):
        self.n = n
        self.q = q
        f = math.factorial
        size = math.floor(f(n) / f(q) / f(n-q))
        self.r = size
        self.c = size
        self.m = numpy.zeros([self.r,self.c],float)
        for i in range(0,self.r):
            for j in range(0,self.c):
                if (i==j):
                    self.m[i,j] = 1.0;

        self.m = numpy.matrix([[1, 2], [2, 1]])

    def ev(self):
        w, v = LA.eigh(self.m);
        return w;

    def power(self, p):
        w, v = LA.eigh(self.m)
        # eigenvector matrix
        P = numpy.matrix(v)
        # Diagonal = (P^t)MP
        D = numpy.transpose(P) * self.m * P
        for i in range (0,self.r):
            D[i,i]=pow(D[i,i],p)
        D = P * D * numpy.transpose(P)
        return D

    @staticmethod
    def fromBaseN(n,t):
        """
        :param n: - the base
        :param t: - tuple representin coordinates in base n
        :return: - decimal number
        """
        sum = 0
        p = len(t) - 1
        for i in t:
            sum += i*(pow(n,p))
            p = p - 1
        return sum

    @staticmethod
    def toBaseN(n,q,d):
        """
        :param n: base we work in
        :param q: number of digits in the vector
        :param d: decimal number to move to new base as tuple
        :return:
        """
        l = [0]*(q)
        for i in range(0,q):
            l[i] = int(d%n)
            d=math.floor(d/n)
        l.reverse()
        return tuple(l)



def test():
    m = matrix(2,1)
    #t = (1,0,0)
    #print(m.fromBaseN(2,t))
    #print(m.toBaseN(2,3,4))
    print(m.power(3))


test()











