import math
import numpy
from numpy import linalg as LA
import sympy
import calculations
import itertools

class matrix(object):
    def __init__(self, n, q, isSymbolic):
        self.n = n
        self.q = q
        f = math.factorial
        size = int(math.floor(f(n) / f(n-q)))
        self.r = size
        self.c = size

        # choose matrix type
        self.isSymbolic = isSymbolic
        if (isSymbolic == True):
            self.m=sympy.Matrix(numpy.zeros([self.r,self.c]))
        else:
            self.m=numpy.zeros([self.r,self.c],dtype=numpy.float64)

        self.indicesToVectors = []
        self.vectorsToIndices = {}
        self.unhandledTypes = {}

        # build map vector <-> matrix index
        i = 0;
        for v in itertools.permutations(range(n), q):
            self.indicesToVectors.append(v)
            self.vectorsToIndices[v] = i
            i = i + 1

        # init matrix with base values
        for i in range(0,self.r):
            alpha = self.indicesToVectors[i]
            for j in range(0,self.c):
                beta = self.indicesToVectors[j]
                self.m[i,j] = calculations.calculate_benes(alpha, beta, n)


    def getProbAlphaBeta(self, alpha, beta):
        i = self.vectorsToIndices(alpha)
        j = self.vectorsToIndices(beta)
        return self.m[i,j]

    def getEigenvalues(self):
        if (self.isSymbolic == True):
            w = self.m.eigenvals();
        else:
            w, v = LA.eigh(self.m);
            #w,v = scipy.linalg.eig(self.m)

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

    def checkPorbQ3(self):
        count = 0
        for i in range(0,self.r):
            alpha = self.indicesToVectors[i]
            for j in range(0,self.c):
                beta = self.indicesToVectors[j]
                expected = self.getExpectedProb(alpha,beta)
                if (expected == 0):
                    count = count + 1
                #if (expected != self.m[i,j]):
                    #print (str(alpha) + "->" + str(beta))
        return count

    def checkProbQ2(self, p):
        probs = [float(pow(2.0,float(i))/pow(8.0,3.0) + (1.0/pow(8.0,2.0))) for i in range(1,4)]
        probs.append(float(1.0/(pow(8.0,2.0))))
        if (p in probs):
            return True
        return False


    def getEigenvalueSet(self):
        return set(self.getEigenvalues())

    def getRoundEigevalueSet(self):
        return set(numpy.round(self.getEigenvalues(),4))

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

    @staticmethod
    def lowestSet(int_type):
        low = (int_type & -int_type)
        lowBit = -1
        while (low):
            low >>= 1
            lowBit += 1
        return(lowBit)

    def getType(self, n,m):
        """
        return the lowest bit of difference between two numbers
        :param n:
        :param m:
        :return:
        """
        return 1 + self.lowestSet(n^m)

    def getTripletType(self, t):
        """
        returns the type of a triplet, based on diffrences of it's members
        :param t:
        :return:
        """
        type = [0,0,0]
        type[0] = self.getType(t[0],t[1])
        type[1] = self.getType(t[0],t[2])
        type[2] = self.getType(t[1],t[2])
        return type

    @staticmethod
    def isdrr(t):
        """
        is of type [d,r,r]
        :param t:
        :return:
        """
        if ((t[0] > t[1]) & (t[1] == t[2])):
            return True
        return False

    @staticmethod
    def iskll(t):
        """
        is of type [k,l,l]
        :param t:
        :return:
        """
        if ((t[0] > t[1]) & (t[1] == t[2])):
            return True
        return False

    @staticmethod
    def islkl(t):
        if ((t[0] == t[2]) & (t[1] > t[2])):
            return True
        return False

    @staticmethod
    def isllk(t):
        if ((t[0] == t[1]) & (t[2] > t[0])):
            return True
        return False

    def get_kl(self, t):
        """
        given a some sort of kl triplet, retunrs specific values
        :param t:
        :return:
        """
        if (self.isllk(t)):
            return (t[2],t[1])
        if (self.islkl(t)):
            return (t[1],t[1])
        if (self.iskll(t)):
            return (t[0],t[2])
        print "get kl" + str(t)

    def get_dr(self, t):
        if (self.isdrr(t)):
            return (t[0],t[1])
        print "get dr" + str(t)

    def getExpectedProb(self, t1, t2):
        tt1 = self.getTripletType(t1)
        tt2 = self.getTripletType(t2)

        if ((self.isdrr(tt1)) & (self.iskll(tt2))):
            d,r = self.get_dr(tt1)
            k,l = self.get_kl(tt2)

            if ((d != k) & (d != l) & (r != k) & (r != l)):
                return (float(1.0/(pow(8.0,3.0))))
            if ((k == d) & (l != r)):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,d)/(pow(8.0,4.0))))
            if ((k == d) & (l == r)):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,d)/(pow(8.0,4.0))) + float(2*(pow(2.0,r)/(pow(8.0,4.0)))) + float(2*(pow(2.0,d+r)/(pow(8.0,5.0)))))
            if (k == r):
                return (float(1.0/(pow(8.0,3.0))))
            if (l == d):
                return (float(1.0/(pow(8.0,3.0))))
            if (l == r):
                return (float(1.0/(pow(8.0,3.0))) + float(2*(pow(2.0,r)/(pow(8.0,4.0)))))

        if (((self.isdrr(tt1)) & (self.isllk(tt2))) | ((self.isdrr(tt1)) & (self.islkl(tt2)))):
            d,r = self.get_dr(tt1)
            k,l = self.get_kl(tt2)

            if ((d != k) & (d != l) & (r != k) & (r != l)):
                return (float(1.0/(pow(8.0,3.0))))
            if ((k == d) & (l != r)):
                return (float(1.0/(pow(8.0,3.0))))
            if ((k == d) & (l == r)):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,r)/(pow(8.0,4.0))) + float(pow(2.0,r+d)/(pow(8.0,5.0))))
            if (k == r):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,r)/(pow(8.0,4.0))))
            if (l == d):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,d)/(pow(8.0,4.0))))
            if (l == r):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,r)/(pow(8.0,4.0))))

        if (((self.isdrr(tt2)) & (self.isllk(tt1))) | ((self.isdrr(tt2)) & (self.islkl(tt1)))):
            d,r = self.get_dr(tt2)
            k,l = self.get_kl(tt1)

            if ((d != k) & (d != l) & (r != k) & (r != l)):
                return (float(1.0/(pow(8.0,3.0))))
            if ((k == d) & (l != r)):
                return (float(1.0/(pow(8.0,3.0))))
            if ((k == d) & (l == r)):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,r)/(pow(8.0,4.0))) + float(pow(2.0,r+d)/(pow(8.0,5.0))))
            if (k == r):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,r)/(pow(8.0,4.0))))
            if (l == d):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,d)/(pow(8.0,4.0))))
            if (l == r):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,r)/(pow(8.0,4.0))))

        # [l,k,l] -> [l,k,l]
        if ((self.islkl(tt2)) & (self.islkl(tt1))):
            d,r = self.get_kl(tt1)
            k,l = self.get_kl(tt2)

            if ((k == d) & (l == r)):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,k)/(pow(8.0,4.0))) + float(2*(pow(2.0,l)/(pow(8.0,4.0)))) + float(2*(pow(2.0,k+l)/(pow(8.0,5.0)))))

        # [l,l,k] -> [l,l,k]
        if ((self.isllk(tt2)) & (self.isllk(tt1))):
            d,r = self.get_kl(tt1)
            k,l = self.get_kl(tt2)

            if ((k == d) & (l == r)):
                return (float(1.0/(pow(8.0,3.0))) + float(pow(2.0,d)/(pow(8.0,4.0))) + float(2*(pow(2.0,r)/(pow(8.0,4.0)))) + float(2*(pow(2.0,d+r)/(pow(8.0,5.0)))))
            else: #l,l,k -> r,r,d !
                return (float(1.0/(pow(8.0,3.0))))

        if ((self.islkl(tt1)) & (self.isllk(tt2))):
            return 0

        if ((self.isllk(tt1)) & (self.islkl(tt2))):
            return 0

        if ((self.islkl(tt1)) & (self.islkl(tt2))):
            return 0

        v = str(t1) + "->" + str(t2)
        k = str(tt1) + "->" + str (tt2)
        if (k not in self.unhandledTypes):
            self.unhandledTypes[k]=v
        return 0

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


def test_probs():
    m = matrix(8,1)
    print m.getExpectedProb((0, 1, 3),(0, 4, 1))

def test_q2():
    m = matrix(8,2,True)
    print m.getEigenvalues()

def test_q3():
    m = matrix(8,3,False)
    #print m.checkPorbQ3();
    #print m.unhandledTypes
    print m.getRoundEigevalueSet()
    #print m.getEigenvalues()

test_q3()