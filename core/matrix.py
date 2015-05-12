import math
import numpy
from numpy import linalg as LA
import sympy
import calculations
import itertools

class matrix(object):
    def __init__(self, n, q):
        self.n = n
        self.q = q
        f = math.factorial
        size = int(math.floor(f(n) / f(n-q)))
        self.r = size
        self.c = size
        self.m=sympy.Matrix(numpy.zeros([self.r,self.c]))
        self.indicesToVectors = []
        self.vectorsToIndices = {}

        # build map vector -> matrix index
        # build map
        i = 0;
        for v in itertools.permutations(range(n), q):
            # build map matrix index -> vector
            self.indicesToVectors.append(v)
            # build map vector -> matrix index
            self.vectorsToIndices[v] = i
            i = i + 1

        # init matrix with base values
        for i in range(0,self.r):
            alpha = self.indicesToVectors[i]
            for j in range(0,self.c):
                beta = self.indicesToVectors[j]
                self.m[i,j] = calculations.calculate_benes_2(alpha, beta, n)
                if self.checkProbQ2(self.m[i,j]) is False:
                    print self.m[i,j]
        # fill in symmetric part
        #t = self.m.transpose()
        #numpy.fill_diagonal(t,0)
        #self.m = self.m + t

    def getProbAlphaBeta(self, alpha, beta):
        i = self.vectorsToIndices(alpha)
        j = self.vectorsToIndices(beta)
        return self.m[i,j]

    def getEigenvalues(self):
        #w, v = LA.eigh(self.m);
        #w,v = scipy.linalg.eig(self.m)
        w = self.m.eigenvals();
        return w;

    def getDiagonal(self):
        w, v = LA.eigh(self.m)
        # eigenvector matrix
        P = numpy.matrix(v)
        # Diagonal = (P^t)MP
        D = numpy.transpose(P) * self.m * P
        return D

    # exponentiate matrix
    def getMatrixPower(self, p):
        w, v = LA.eigh(self.m)
        # eigenvector matrix
        P = numpy.matrix(v)
        # Diagonal = (P^t)MP
        D = numpy.transpose(P) * self.m * P
        for i in range (0,self.r):
            D[i,i]=pow(D[i,i],p)
        D = P * D * numpy.transpose(P)
        return D

    def checkProbQ2(self, p):
        probs = [float(pow(2.0,float(i))/pow(8.0,3.0) + (1.0/pow(8.0,2.0))) for i in range(1,4)]
        probs.append(float(1.0/(pow(8.0,2.0))))
        if (p in probs):
            return True
        return False

    def getEigenvalueSet(self):
        return set(self.getEigenvalues())

    def getRoundEigevalueSet(self):
        return set(numpy.round(self.getEigenvalues(),14))

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

    def findUnsymPair(self):
        for i in range(0,self.r):
            for j in range(0,self.c):
                if (self.m[i,j] != self.m[j,i]):
                    print self.toBaseN(self.n, self.q, i), ("->",), self.toBaseN(self.n, self.q, j)


def test():
    m = matrix(8,2)
    #print m.isSymmetric()
    #print(m.power(3))
    #print m.getDiagonal()
    print m.getEigenvalues()
    #print m.getEigenvalueSet()
    #print m.getRoundEigevalueSet()
test()











