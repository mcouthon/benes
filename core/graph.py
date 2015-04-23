"""List of strongly connected components - a list of edges"""

class Switch:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Edge:
    def __init__(self, switch1, switch2, cross_half, switch1_index):
        self.switch1 = switch1
        self.switch2 = switch2
        self.cross_half = cross_half
        self.switch1_index = switch1_index


def validate(a, b, n):
    """
    :param a:
    :param b:
    :param n:
    :return: Whether given parameters are as expected
    """
    if (b != a):
        print "Alpha and beta are not consistent"
        return False
    if (n % 2 == 1):
        print "N must be even"
        return False
    return True


def get_containing_switch(switches, ball):
    """
    :param switches:
    :param ball:
    :return: First switch containing the given ball, at any index
    """
    for switch in switches:
        if (switch.start == ball or switch.end == ball):
            return switch
    return None


def get_list_of_edges(alpha, beta, n):
    """
    :param alpha:
    :param beta:
    :param n:
    :return: List of edges that should be in the switch graph matching the permutation
    """
    if (not validate(alpha.length, beta.length, n)):
        return

    switches = []
    for i in range(n/2):
        switches[i] = Switch(i, n/2 + i)

    edges = []
    for i in range(alpha.length):
        cross_half = 0 if (beta[i] - alpha[i] < n/2) else 1
        switch1_index = 0 if (alpha[i] < n/2) else 1
        switch1 = get_containing_switch(switches, alpha[i])
        switch2 = get_containing_switch(switches, beta[i])
        edges.append(Edge(switch1, switch2, cross_half, switch1_index))
    return edges
