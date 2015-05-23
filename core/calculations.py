import time
from core.graph import get_sccs, get_diff_index
from benes_3 import calculate_benes_3

ON = 1
OFF = 0


def calculate_benes(alpha, beta, n):
    """
    Calculate the probability of an ordered set alpha to get to the ordered set beta
    with n being the current size of the net
    """
    if not alpha:
        return 1.0

    if n == 2:
        return 0.5

    sccs = get_sccs(alpha, beta, n)
    return calculate_all(alpha, beta, sccs, n)


def calculate_all(alpha, beta, sccs, n):
    """
    Traverse all possible permutations of switches/SCCs, and recursively calculate the probability
     n
    B
     (alpha->beta)
    """
    benes_sum = 0
    half_n = n / 2
    denom = 1.0 / (2 ** get_num_of_switches(sccs))

    for perm in range(2 ** len(sccs)):
        # Get the states of all the *relevant* switches
        top_switches = calculate_switches(sccs, perm)
        alpha_left = []
        alpha_right = []
        beta_left = []
        beta_right = []

        for i in range(len(alpha)):
            src = alpha[i]
            dest = beta[i]

            switch_state = top_switches[src if src < half_n else src - half_n]
            update_alphas_and_betas(src, dest, switch_state, alpha_left, beta_left, alpha_right, beta_right, half_n)

        benes_sum += calculate_benes(alpha_left, beta_left, half_n) * calculate_benes(alpha_right, beta_right, half_n)

    return denom * benes_sum


def get_num_of_switches(sccs):
    """
    Returns the total number of *unique* switches involved
    """
    unique_switches = set()
    num_of_switches = 0
    for j in range(len(sccs)):
        scc = sccs[j]
        for sub_scc in scc:
            for switch in sub_scc:
                if switch not in unique_switches:
                    unique_switches.add(switch)
                    num_of_switches += 1

    return num_of_switches


def update_alphas_and_betas(src, dest, switch_state, alpha_left, beta_left, alpha_right, beta_right, half_n):
    """
    Depending on the state of the switch and the source value, add to/from values to either the
    left or the right side, for the recursion
    """
    dest = dest if dest < half_n else dest - half_n

    if switch_state == ON:
        if src < half_n:
            alpha_right.append(src)
            beta_right.append(dest)
        else:
            alpha_left.append(src - half_n)
            beta_left.append(dest)
    else:
        if src < half_n:
            alpha_left.append(src)
            beta_left.append(dest)
        else:
            alpha_right.append(src - half_n)
            beta_right.append(dest)


def calculate_switches(sccs, perm):
    """
    Create maps from top switches to their current state, dependant on
    the SCCs and the current permutation
    """
    # Create an empty lists for the top/bottom switches
    top_switches = dict()

    for j in range(len(sccs)):
        scc = sccs[j]

        # Get the j'th bit
        bit = 1 << j

        # If the j'th bit in i is up, this scc should start from an on switch
        starting_state = ON if bin(perm & bit)[2] == '1' else OFF

        # Iterate over
        for sub_scc in scc:
            for switch in sub_scc:
                # Update the value of the switch
                if switch.top:
                    top_switches[switch.left] = starting_state
            # Flip the state, because we've passed a dotted edge
            starting_state = ON if starting_state == OFF else OFF

    return top_switches


def calculate_benes_2(alpha, beta, n):
    if len(alpha) != 2:
        raise StandardError("Alpha is not of length 2")

    d = get_diff_index(alpha[0], alpha[1])
    r = get_diff_index(beta[0], beta[1])

    result = 1.0 / (n ** 2)

    if d != r:
        return result
    else:
        return result + (2.0 ** d) / (n ** 3)






def runner_2(n=8, repetitions=1):
    # for i in itertools.repeat(None, repetitions):
    for i in range(repetitions):
        t1 = time.time()
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(n):
                        if a == b or c == d:
                            continue

                        c1 = calculate_benes((a, b), (c, d), n)
                        c2 = calculate_benes_2((a, b), (c, d), n)

                        if c1 != c2:
                            print "Incorrect value for: (%s, %s) -> (%s, %s)" % (a, b, c, d)
        print 'Repetition no.', i + 1, time.time() - t1


def runner_3(n=8, repetitions=1):
    # for i in itertools.repeat(None, repetitions):
    for i in range(repetitions):
        t1 = time.time()
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(n):
                        for e in range(n):
                            for f in range(n):
                                if a == b or a == c or b == c or d == e or d == f or e == f:
                                    continue

                                c1 = calculate_benes((a, b, c), (d, e, f), n)
                                c2 = calculate_benes_3((a, b, c), (d, e, f), n)

        print 'Repetition no.', i + 1, time.time() - t1


if __name__ == '__main__':
    alpha = (1, 2, 5)
    beta = (4, 5, 1)
    n = 8

    c1 = calculate_benes(alpha, beta, n)
    c2 = calculate_benes_3(alpha, beta, n)

    print c1
    print c2
