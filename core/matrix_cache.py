import os
import cPickle

from core import matrix

ALL_MATRICES_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, 'all_matrices.pkl'))

def get_matrix(*args):
    all_matrices = cPickle.load(open(ALL_MATRICES_PATH, 'rb'))
    if args not in all_matrices:
        all_matrices[args] = matrix.matrix(*args)
        cPickle.dump(all_matrices, open(ALL_MATRICES_PATH, 'wb'))
    return all_matrices[args]

def clear_cache():
    cPickle.dump({}, open(ALL_MATRICES_PATH,'wb'), cPickle.HIGHEST_PROTOCOL)