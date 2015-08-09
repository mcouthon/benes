import math
import numpy
from numpy import linalg as LA
import sympy
from sympy.core.symbol import Dummy
from sympy.simplify.simplify import nsimplify
import calculations
import itertools
import q_vec
#import scipy
#import scipy.linalg

class matrix_factory(object):
    @staticmethod
    def get_probability_matrix(n, q, isSymbolic):
        """
        :param n: vector size
        :param q: tuple size
        :param isSymbolic: determines wether caclulcation will be Symbolic or float128 precision
        :return: returns a matrix instace of size (n)_q with benesh probabilities
        """
        matrix_instance = matrix()
        matrix_instance.n = n
        matrix_instance.q = q
        size = int(math.floor(math.factorial(n) / math.factorial(n-q)))     # (n)_q
        matrix_instance.r = size                                                       # rows
        matrix_instance.c = size                                                       # cols
        matrix_instance.isSymbolic = isSymbolic
        matrix_instance.matrix_type = 'BENESH'
        if (isSymbolic == True):                                            # choose matrix type
            matrix_instance.m=sympy.Matrix(numpy.zeros([matrix_instance.r,matrix_instance.c]))
        else:
            matrix_instance.m=numpy.zeros([matrix_instance.r,matrix_instance.c],dtype=numpy.float64)

        matrix_instance.indicesToVectors = []
        matrix_instance.vectorsToIndices = {}

        i = 0                                                              # build map vector <-> matrix index
        for v in itertools.permutations(range(n), q):
            matrix_instance.indicesToVectors.append(v)
            matrix_instance.vectorsToIndices[v] = i
            i = i + 1

        for i in range(0, matrix_instance.r):                               # init matrix with base values
            alpha = matrix_instance.indicesToVectors[i]
            for j in range(0, matrix_instance.c):
                beta = matrix_instance.indicesToVectors[j]
                matrix_instance.m[i, j] = calculations.calculate_benes(alpha, beta, n)

        return matrix_instance

    @staticmethod
    def get_probability_disk_matrix(n, q, isSymbolic):
        """
        using disk memory and not RAM memory.

        :param n: vector size
        :param q: tuple size
        :param isSymbolic: determines wether caclulcation will be Symbolic or float128 precision
        :return: returns a matrix instace of size (n)_q with benesh probabilities
        """
        import h5py

        matrix_instance = matrix()
        matrix_instance.n = n
        matrix_instance.q = q
        size = int(math.floor(math.factorial(n) / math.factorial(n-q)))     # (n)_q
        matrix_instance.r = size                                                       # rows
        matrix_instance.c = size                                                       # cols
        matrix_instance.isSymbolic = isSymbolic
        matrix_instance.matrix_type = 'BENESH'
        if (isSymbolic == True):                                            # choose matrix type
            matrix_instance.m=sympy.Matrix(numpy.zeros([matrix_instance.r,matrix_instance.c]))
        else:
            f = h5py.File("/tmp/mytestfile.hdf5", "w")
            matrix_instance.f = f
            matrix_instance.m = f.create_dataset("mydataset", 
                                                 (matrix_instance.r,matrix_instance.c),
                                                 dtype=numpy.float64)
            # numpy.zeros([matrix_instance.r,matrix_instance.c],dtype=numpy.float64)

        matrix_instance.indicesToVectors = []
        matrix_instance.vectorsToIndices = {}

        i = 0                                                              # build map vector <-> matrix index
        for v in itertools.permutations(range(n), q):
            matrix_instance.indicesToVectors.append(v)
            matrix_instance.vectorsToIndices[v] = i
            i = i + 1

        for i in range(0, matrix_instance.r):                               # init matrix with base values
            alpha = matrix_instance.indicesToVectors[i]
            for j in range(0, matrix_instance.c):
                beta = matrix_instance.indicesToVectors[j]
                matrix_instance.m[i, j] = calculations.calculate_benes(alpha, beta, n)

        return matrix_instance

    @staticmethod
    def get_reduced_matrix(n, q, isSymbolic):


        qv = q_vec.q_vec(n, q)
        columns = qv.build_reduced_matrix()

        matrix_instance = matrix()
        matrix_instance.n = n
        matrix_instance.q = q

        if (isSymbolic == True):                                            # choose matrix type
            matrix_instance.m=sympy.Matrix(numpy.matrix(columns))
        else:
            matrix_instance.m=numpy.matrix(columns)

        #matrix_instance.m = numpy.matrix(columns)

        size = int(math.floor(math.factorial(n) / math.factorial(n-q)))     # (n)_q
        matrix_instance.r = len(columns)                                  # rows
        matrix_instance.c = len(columns)                                  # cols
        matrix_instance.isSymbolic = isSymbolic
        matrix_instance.matrix_type = 'REDUCED'

        return matrix_instance

class matrix(object):
    """
    matrix class, wrapper for linear algebra calculations in the project
    """
    def __init__(self):
        return

    def get_size(self):
        return self.r

    def get_symbol_by_index(self,i):
        return self.indicesToVectors[i]

    def get_probability_for_symbols(self, t1, t2):
        """
        return the probability to move from symbol (q-tuple or type) , from the matrix
        :param t1: symbolic tuple (q-tuple or type)
        :param t2:
        :return:
        """
        if (self.matrix_type == 'BENESH'):
            i = self.vectorsToIndices[t1]
            j = self.vectorsToIndices[t2]
        elif (self.matrix_type == 'REDUCED'):
            i = 0;
            j = 0;
        return self.m[i,j]

    def get_eigenvalues(self):
        """
        returns the eigenvalues of the matrix,
        using the appropriate libraries, based on the symbolism
        :return:
        """
        if (self.isSymbolic == True):
            w = self.m.eigenvals()
        else:
            w,v = LA.eigh(self.m)
            #w,v = scipy.linalg.eig(self.m)
        return w;

    def get_diagonal(self):
        """
        returns the diagonal form of the matrix
        :return:
        """
        if (self.isSymbolic == True):
            P, D = self.m.diagonalize();
            return D
        else:
            w, v = LA.eigh(self.m)
            P = numpy.matrix(v)
            D = numpy.transpose(P) * self.m * P
            return D

    def getMatrixPower(self, p, compute_diagonal=True):
        """
        Diagonlizes the matrix, and exponentiates it efficiently.
        returns the matrix p-th power.
        :param p:
        :return:
        """
        if compute_diagonal:
            if (self.isSymbolic == False):
                w, v = LA.eigh(self.m)
                P = numpy.matrix(v)
                D = numpy.transpose(P) * self.m * P
                for i in range (0,self.r):
                    D[i,i]=pow(D[i,i],p)
                D = P * D * numpy.transpose(P)
                return D
            else:
                P, D = self.m.diagonalize();
                for i in range (0,self.r):
                    D[i,i]=pow(D[i,i],p)
                D = P * D * P^(-1)
                return D
        else:
            return self.m^p

    def get_eigenvalue_set(self):
        """
        returns a set of eigenvalues for the matrix
        :return:
        """
        return set(self.get_eigenvalues())

    def get_round_eigevalue_set(self):
        """
        returns a set of rounded (decimal precsion) eigenvalues
        :return:
        :return:
        """
        if (self.isSymbolic == True):
            return self.get_eigenvalues()
        else:
            return set(numpy.round(self.get_eigenvalues(), 4))

    """
    Benesh probabilities utils
    """

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

    def custom_charpoly(self, **flags):
        """
        custom charpoly
        """

        if (self.isSymbolic == True):
            self.m = self.m._new(self.m.rows, self.m.cols,[nsimplify(v, rational=True) for v in self.m])
            max_denom = 0;
            for i in range (0,self.m.rows):
                for j in range (0,self.m.cols):
                    if self.m[i,j] > max_denom:
                        max_denom = self.m[i,j].q
            print max_denom
            self.m *= max_denom
            flags.pop('simplify', None)  # pop unsupported flag
            return self.m.berkowitz_charpoly(Dummy('x'))
        else:
            numpy.rint(self.m)
            return numpy.rint(numpy.poly(self.m))




