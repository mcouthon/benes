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


def get_list_of_edges(alpha, beta, n):
    q = alpha.length
    if (beta != q):
        print "Alpha and beta are not consistent"
        return []
