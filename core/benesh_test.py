from sympy.polys.polytools import div
from matrix import matrix_factory
import matrix_cache
import calculations
import benes_3
import time
from sympy import Symbol
from sympy import Poly
from sympy import pdiv
import differences
import sympy
import numpy
from sympy.simplify.simplify import nsimplify

"""
Tests
"""
def test_eigs(n,q,isSymbolic):
    print "n=: " + str(n) + ", q: " + str(q) + ", isSymbolic : " + str(isSymbolic)
    m = matrix_factory.get_reduced_matrix(n, q, isSymbolic)
    print "Rounded eigs: " + str(m.get_round_eigevalue_set())
    print "All eigs: " + str(m.get_eigenvalue_set())

def test_reduced(n,q,isSymbolic):
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Testing Matrix"
    print "Matrix Type = Reduced (only types)"
    print "n = " + str(n)
    print "q = " + str(q)
    precision = "Float"
    if isSymbolic:
        precision = "Decimal"
    print "precision = " + precision
    m = matrix_factory.get_reduced_matrix(n,q,isSymbolic)
    print "All eigs: " + str(m.get_round_eigevalue_set())

    #print "All eigs: " + str(m.get_eigenvalue_set())
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

def runner_q2(n=8, repetitions=1):
    for i in range(repetitions):
        t1 = time.time()
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(n):
                        if a == b or c == d:
                            continue

                        c1 = calculations.calculate_benes((a, b), (c, d), n)
                        c2 = calculations.calculate_benes((a, b), (c, d), n)

                        if c1 != c2:
                            print "Incorrect value for: (%s, %s) -> (%s, %s)" % (a, b, c, d)
        print 'Repetition no.', i + 1, time.time() - t1

def runner_q3(n=8, q=3, isSymbolic = False, repetitions=1):
    unhandled_types = {}
    for i in range(repetitions):
        m = matrix_factory.get_probability_matrix(n, q, isSymbolic)
        for i in range(0, m.get_size()):
            for j in range(0, m.get_size()):
                alpha = m.get_symbol_by_index(i)
                beta = m.get_symbol_by_index(j)
                expected = benes_3.calculate_benes_3(alpha, beta, n)
                actual = m.get_probability_for_symbols(alpha, beta)
                if expected != actual:
                    add_to_unexpected(alpha, beta, unhandled_types, expected, actual)

        print "Unexpected probabilities: "
        print unhandled_types

def add_to_unexpected(alpha, beta, ex_set, ex, actual):
    tt1 = benes_3.get_triplet_type(alpha)
    tt2 = benes_3.get_triplet_type(beta)
    v = str(alpha) + "->" + str(beta) + "expected: " + str(ex) + "actual:" + str(actual)
    k = str(tt1) + "->" + str(tt2)
    if k not in ex_set:
        ex_set[k] = v

def get_char_poly(n ,q):
    m = matrix_factory.get_reduced_matrix(n,q,True)
    print "got matrix"
    p = m.custom_charpoly()
    print p


def test_char_poly(n, q):
    m = matrix_factory.get_reduced_matrix(n,q,True)
    print "got matrix"
    p = m.custom_charpoly()
    x = Symbol('x')
    p = p.as_expr(x)
    for root in (1, 1.0 / 8, 1.0 / 8):
        print p
        assert p.subs(x,root) == 0
        p = div(p,Poly(x-root,x))[0]
        p = p.as_expr(x)
    print p

def get_float_poly(n,q):

    m = matrix_factory.get_reduced_matrix(n,q,False)
    m.m *= 8
    print "got matrix"
    print m.get_size()
    p = m.custom_charpoly()
    print p

def get_nullspace(n,q,eigv):
    M = matrix_cache.get_reduced_matrix(n,q, True)
    M.m = M.m._new(M.m.rows, M.m.cols,[nsimplify(v, rational=True) for v in M.m])

    # N = M - lambdaI
    N = M.m - sympy.Matrix.eye(M.get_size())* eigv

    # rationalize entries
    N = N._new(N.rows, N.cols,[nsimplify(v, rational=True) for v in N])

    # find eigenspace - Kernel(M-lambdaI) = Kernel(N)
    EigenSpaceBase = N.nullspace()

    # orthogonal space = Kernel(TransposedEigenVectors)
    TransposedEigenSpaceBase = [list(v) for v in EigenSpaceBase]
    EigenSpaceTransposeMatrix = (sympy.Matrix(numpy.matrix(TransposedEigenSpaceBase)))
    OrthogonalSubspaceBase = EigenSpaceTransposeMatrix.nullspace()

    # need to transpose to put the vectors in columns, and get a matrix for the orthogonal operator
    OrthogonalSubspaceMatrix = (sympy.Matrix(numpy.matrix(OrthogonalSubspaceBase))).transpose()

    # multiply M * Ortohogonal, to get the reduction of M on the orthogonal subspace
    OrthogonalSubspaceMatrix =  OrthogonalSubspaceMatrix._new(OrthogonalSubspaceMatrix.rows, OrthogonalSubspaceMatrix.cols,
                                                              [nsimplify(v, rational=True) for v in OrthogonalSubspaceMatrix])
    EigenValueReducedMatrix = M.m * OrthogonalSubspaceMatrix
    EigenValueReducedMatrix = EigenValueReducedMatrix.rref()




if __name__ == '__main__':
    get_nullspace(8, 2, (1/8.0))

