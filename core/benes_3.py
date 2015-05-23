def get_type(n, m):
    """
    return the lowest bit of difference between two numbers
    """
    int_type = n ^ m
    low = (int_type & -int_type)
    low_bit = -1
    while low:
        low >>= 1
        low_bit += 1
    return low_bit + 1

def get_triplet_type(triplet):
    """
    returns the type of a triplet, based on differences of it's members
    """
    t_type = [0, 0, 0]
    t_type[0] = get_type(triplet[0], triplet[1])
    t_type[1] = get_type(triplet[0], triplet[2])
    t_type[2] = get_type(triplet[1], triplet[2])
    return t_type

def get_triplet_numbers(triplet_type):
    """
    Returns r and d (or k and l) of a certain triplet type
    """
    a, b, c = triplet_type[0], triplet_type[1], triplet_type[2]

    if a > b:
        return b, a
    elif a < b:
        return a, b
    elif a < c:
        return a, c
    else:
        return c, a

def calculate_benes_3(alpha, beta, n):
    alpha_type = get_triplet_type(alpha)
    beta_type = get_triplet_type(beta)

    r, d = get_triplet_numbers(alpha_type)
    l, k = get_triplet_numbers(beta_type)

    if alpha_type == beta_type:
        if k == d and l == r:
            return 1.0 / (n ** 3) + (2.0 ** d) / (n ** 4) + 2 * (2.0 ** r) / (n ** 4) + 2 * (2.0 ** (d + r)) / (n ** 5)
        elif k == d and l != r:
            return 1.0 / (n ** 3) + (2.0 ** d) / (n ** 4)
        elif k == r:
            return 1.0 / (n ** 3)
        elif l == d:
            return 1.0 / (n ** 3)
        elif l == r:
            return 1.0 / (n ** 3) + 2 * (2.0 ** r) / (n ** 4)
        else:
            return 1.0 / (n ** 3)

    else:
        if k == d and l == r:
            return 1.0 / (n ** 3) + (2.0 ** r) / (n ** 4) + (2.0 ** (d + r)) / (n ** 5)
        elif k == d and l != r:
            return 1.0 / (n ** 3)
        elif k == r:
            return 1.0 / (n ** 3) + (2.0 ** r) / (n ** 4)
        elif l == d:
            return 1.0 / (n ** 3) + (2.0 ** d) / (n ** 4)
        elif l == r:
            return 1.0 / (n ** 3) + (2.0 ** r) / (n ** 4)
        else:
            return 1.0 / (n ** 3)
