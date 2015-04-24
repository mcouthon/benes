import math
import numpy
from numpy import linalg as LA
import calculations

class matrix(object):
    def nCr(n,r):
        f = math.factorial
        return f(n) / f(r) / f(n-r)

    def __init__(self, n, q):
        self.n = n
        self.q = q
        f = math.factorial
        size = int(math.floor(f(n) / f(n-q)))
        self.r = size
        self.c = size
        self.m = numpy.zeros([self.r,self.c],float)
        print "Matrix Size: " + str(self.r) + "x" + str(self.c)
        # calculate upper diagonal matrix
        for i in range(0,self.r):
            alpha = self.toBaseN(self.n,self.q,i)
            for j in range(i,self.c):
                beta = self.toBaseN(self.n,self.q,j)
                #print alpha + ("->",) + beta
                self.m[i,j] = calculations.calculate_benes(alpha, beta, n);
        # fill in symmetric part
        t = self.m.transpose()
        numpy.fill_diagonal(t,0)
        self.m = self.m + t

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

    def isSymmetric(self):
        return numpy.allclose(self.m.transpose(), self.m)

    def P_alpha_beta(self, alpha,beta):
        i = self.fromBaseN(self.n,alpha)
        j = self.fromBaseN(self.n,beta)
        return self.m[i,j]



def test():
    m = matrix(8,2)
    print m.m
    print m.isSymmetric()
    print m.ev()
    #print(m.power(3))
test()











