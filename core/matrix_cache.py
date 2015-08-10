"""
caching matrices in files, so you won't have to run the whole calculation of the benesh-matrix from scratch every time.
"""

import os
import cPickle

from core import matrix

ALL_MATRICES_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, 'all_matrices.pkl'))
ALL_RED_MATRICES_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, 'all_red_matrices.pkl'))
ALL_CHARPOLY_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, 'all_charpoly.pkl'))


def get_matrix(*args):
    all_matrices = cPickle.load(open(ALL_MATRICES_PATH, 'rb'))
    if args not in all_matrices:
        all_matrices[args] = matrix.matrix_factory.get_probability_matrix(*args)
        cPickle.dump(all_matrices, open(ALL_MATRICES_PATH, 'wb'), cPickle.HIGHEST_PROTOCOL)
    return all_matrices[args]


def get_reduced_matrix(*args):
    all_red_matrices = cPickle.load(open(ALL_RED_MATRICES_PATH, 'rb'))
    if args not in all_red_matrices:
        all_red_matrices[args] = matrix.matrix_factory.get_reduced_matrix(*args)
        cPickle.dump(all_red_matrices, open(ALL_RED_MATRICES_PATH, 'wb'), cPickle.HIGHEST_PROTOCOL)
    return all_red_matrices[args]


def get_char_poly(*args):
    all_charpoly = cPickle.load(open(ALL_CHARPOLY_PATH, 'rb'))
    if args not in all_charpoly:
        print 'getting reduced matrix'
        m = get_reduced_matrix(*args)
        print 'getting charpoly'
        all_charpoly[args] = m.custom_charpoly()
        cPickle.dump(all_charpoly, open(ALL_CHARPOLY_PATH, 'wb'), cPickle.HIGHEST_PROTOCOL)
    return all_charpoly[args]


def clear_cache():
    cPickle.dump({}, open(ALL_MATRICES_PATH, 'wb'), cPickle.HIGHEST_PROTOCOL)
    cPickle.dump({}, open(ALL_RED_MATRICES_PATH, 'wb'), cPickle.HIGHEST_PROTOCOL)
    cPickle.dump({}, open(ALL_CHARPOLY_PATH, 'wb'), cPickle.HIGHEST_PROTOCOL)
