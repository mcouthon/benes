from matrix import matrix_factory
import calculations
import benes_3
import time

"""
Tests
"""
def test_eigs(n,q,isSymbolic):
    print "n=: " + str(n) + "q: " + str(q) + "isSymbolic : " + str(isSymbolic)
    m = matrix_factory.get_probability_matrix(n,q,isSymbolic)
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

if __name__ == '__main__':
    for i in range(2,9):
        test_reduced(8,i,True)
    #test_reduced(8,2,True)
    #runner_q2(8, 1)
    #runner_q3(8, 3)
    #test_eigs(8,2,False)
    #test_eigs(8,2,True)
    #test_eigs(8,3,False)
    #test_reduced(8,3,True)