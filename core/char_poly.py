from math import sqrt
import cPickle
import os
from sympy.polys.polytools import Poly, Symbol, div
from core import matrix_cache

POLYS_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, 'all_polys.pkl'))


class CharPoly(object):
	def __init__(self, n, q):
		self.n = n
		self.x = Symbol('x')
		self.poly = self.create_char_poly(n, q)

	def create_char_poly(self, n, q):
		m = matrix_cache.get_reduced_matrix(n, q, True)
		p = m.m.eigenvals()
		p = p.as_expr(self.x)
		return p.nsimplify()

	def get_char_poly_elements(self):
		result = dict()
		for k in range(self.n):
			root = self.get_root(k)
			if self.sub_root_linear(root) == 0:
				multiplicity = self.get_root_mult(root, is_linear=True)
				result[root] = (multiplicity, k, self.get_root_str_repr(k, multiplicity, True))

			if self.sub_root_sqr(root) == 0:
				multiplicity = self.get_root_mult(root, is_linear=False)
				result[root] = (multiplicity, k, self.get_root_str_repr(k, multiplicity, False))

		return result

	@staticmethod
	def get_root(k):
		return 1.0 / (2 ** k)

	def sub_root_linear(self, root):
		return self.poly.subs(self.x, root)

	def sub_root_sqr(self, root):
		return self.poly.subs(self.x, sqrt(root))

	def get_root_mult(self, root, is_linear):
		mult_count = 0
		if is_linear:
			sub_root = self.sub_root_linear
			div_poly = self.get_div_poly_linear(root)
		else:
			sub_root = self.sub_root_sqr
			div_poly = self.get_div_poly_sqr(root)

		while sub_root(root) == 0:
			mult_count += 1
			self.div_pol(div_poly)

		return mult_count

	def div_pol(self, div_poly):
		self.poly = div(self.poly, div_poly)[0]
		self.poly = self.poly.as_expr(self.x)
		self.poly = self.poly.nsimplify()

	def get_div_poly_linear(self, root):
		return Poly(self.x - root, self.x, domain='QQ')

	def get_div_poly_sqr(self, root):
		return Poly(self.x ** 2 - root, self.x, domain='QQ')

	@staticmethod
	def get_root_str_repr(k, mult, is_linear):
		if is_linear:
			return '(x - 1 / %s)^%s' % (2 ** k, mult)
		else:
			return '(x^2 - 1 / %s)^%s' % (2 ** k, mult)

	def get_roots(self):
		cp_elements = self.get_char_poly_elements()
		return [x[2] for x in cp_elements.values()]

if __name__ == "__main__":
    n = 16
    q = 3
    # cp = CharPoly(n, q)
    # p = cp.poly
    cp = matrix_cache.get_char_poly(n, q, True)
    print cp

