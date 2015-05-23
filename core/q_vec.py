__author__ = 'shira'

import itertools
from typhus import typhus
import math

def lowest_set(int_type):
    low = (int_type & -int_type)
    lowBit = -1
    while (low):
        low >>= 1
        lowBit += 1
    return lowBit

def get_differ_bit(n, m):
    """
    return the lowest bit of difference between two numbers
    :param n:
    :param m:
    :return:
    """
    return 1 + lowest_set(n ^ m)

def inc_type(d):
    d_len = len(d)
    new_d = [x for x in d]
    j = d_len - 1
    while (j > 0) and (new_d[j] == d_len):
        new_d[j] == 1
        j -= 1
    new_d[j] += 1
    return new_d

class q_vec(object):
    def __init__(self, n, q):
        self.n = n
        self.q = q
        self.types = self.generate_types()

    def generate_instances(self):
        vecs = []
        for v in itertools.permutations(range(self.n), self.q):
            vecs.append(v)
        return vecs

    def calculate_type(self, d_vec):
        d = []
        for pair in itertools.combinations(range(self.q), 2):
            d.append(get_differ_bit(d_vec[pair[0]], d_vec[pair[1]]))
        return d

    def generate_types(self):
        # type_len = int(self.q * (self.q - 1) / 2)
        # d_len = int(math.log(self.n))
        # types = [typhus([1 for i in range(type_len)], self)]
        # for i in range(d_len ** type_len):
        #     types.append(typhus(inc_type(types[-1].get_type()), self))
        # return types
        types = []
        for v in self.generate_instances():
            current_type = self.calculate_type(v)
            already_there = False
            for t in types:
                if t.get_type() == current_type:
                    already_there = True
            if not already_there:
                types.append(typhus(current_type, self))
        return types

    def build_reduced_matrix(self):
        reduced_matrix = []
        for d in self.types:
            d_col = []
            for k in self.types:
                d_col.append(d.get_benes_prob(k, self.n) * k.count_instances())
            reduced_matrix.append(d_col)
        return reduced_matrix


"""
Testing
"""
if __name__ == '__main__':
    # q82 = q_vec(8, 2)
    # for c in (q82.build_reduced_matrix()):
    #     print(c)
    # print
    q83 = q_vec(16, 3)
    for c in (q83.build_reduced_matrix()):
        print(c)
    # print
    # q84 = q_vec(8, 4)
    # for c in (q84.build_reduced_matrix()):
    #     print(c)
