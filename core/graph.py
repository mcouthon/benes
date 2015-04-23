"""List of strongly connected components - a list of edges"""

class Switch:
    def __init__(self, start, end, top):
        self.start = start
        self.end = end
        self.top = top

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

def get_all_switches(n):
    switches = []
    for top in [True, False]:
        for i in range(n/2):
            switches[i] = Switch(i, n/2 + i, top)
    return switches

def get_containing_switch(switches, ball, top):
    """
    :param switches:
    :param ball:
    :return: First switch containing the given ball, at any index
    """
    for switch in switches:
        if ((switch.start == ball or switch.end == ball) and switch.top == top):
            return switch
    return None


def get_list_of_edges(alpha, beta, n):
    """
    :param alpha:
    :param beta:
    :param n:
    :return: List of edges that should be in the switch graph matching the permutation
    """
    if (not validate(len(alpha), len(alpha), n)):
        return

    switches = get_all_switches(n)
    edges = []
    for i in range(len(alpha)):
        cross_half = 0 if (beta[i] - alpha[i] < n/2) else 1
        switch1_index = 0 if (alpha[i] < n/2) else 1
        switch1 = get_containing_switch(switches, alpha[i], True)
        switch2 = get_containing_switch(switches, beta[i], False)
        edges.append(Edge(switch1, switch2, cross_half, switch1_index))
    return edges

def get_switch_neighbours(edges, switch, current_dir_down):
    """
    :param edges:
    :param switch:
    :return: All switches that are connected to given switch by an edge
    """
    neighbours = []
    for edge in edges:
        if (current_dir_down and edge.switch2 == switch):
            neighbours.append(edge)
        if (not current_dir_down and edge.switch2 == switch):
            neighbours.append(edge)
    return neighbours

def get_list_of_components(edges, n):
    """
    :param edges:
    :return:
    """
    components = []
    switches = get_all_switches(n)
    queue = []
    while (len(switches) > 0):
        if (len(queue) == 0):
            queue = [edges.pop()]
            components.append([[queue[0].switch1]])
            current_dir_down = True
        current_edge = queue.pop()
        if (current_edge.cross_half):
            components[-1].append([current_edge.switch2])
        else:
            components[-1][-1].append(current_edge.switch2)
        switches.remove(current_edge.switch2)

        for neighbour in get_switch_neighbours(edges, current_edge.switch2):
            if (switches.count(neighbour) > 0):
                switches.remove(neighbour)
                queue.insert(0, neighbour)
    return components