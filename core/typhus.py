import math
import calculations

class typhus(object):
    def __init__(self, d, q):
        self.d = d
        self.q = q
        self.representative = self.generate_representative()

    def get_type(self):
        return self.d

    def generate_representative(self):
        for v in self.q.generate_instances():
            if self.q.calculate_type(v) == self.d:
                return v


    def generate_instances(self):
        d_vecs = []
        for v in self.q.generate_instances():
            if self.q.calculate_type(v) == self.d:
                d_vecs.append(v)
        return d_vecs

    def count_instances(self):
        d_vecs = 0
        for v in self.q.generate_instances():
            if self.q.calculate_type(v) == self.d:
                d_vecs += 1
        return d_vecs

    def get_benes_prob(self, k, n):
        return calculations.calculate_benes(self.representative, k.get_representative(), n)

    def get_representative(self):
        return self.representative