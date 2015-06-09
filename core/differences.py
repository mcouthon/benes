from core import matrix 
from core import matrix_cache

def calc_probability_difference(mat, power=1):
    """
    mat: matrix.matrix
    returns: the probability difference (from uniform )
    """
    size = mat.r
    mat = mat.getMatrixPower(power)
    # math.r is the actual size
    return 0.5 * max(sum(abs(mat[i,j] - (1. / size)) for j in range(size)) for i in range(size))



def get_prob_differences_per_power(mat, max_power):
    diffs = [calc_probability_difference(mat, power) for power in range(1, max_power+1)]
    return diffs

if __name__ == '__main__':
    print 'calculating matrix..'
    # m = matrix.matrix(8,3,False)
    # matrix_cache.clear_cache()
    m = matrix_cache.get_matrix(8, 3, False)
    print 'getting prob differences..'
    print get_prob_differences_per_power(m, 9)
