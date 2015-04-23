"""List of strongly connected components - a list of edges"""


class Switch:
    def __init__(self, left, right, top):
        self.left = left
        self.right = right
        self.top = top


class Edge:
    def __init__(self, switch1, switch2, cross_half, switch1_index):
        self.switches = [switch1, switch2]
        self.cross_half = cross_half
        self.switch1_index = switch1_index


def validate(a, b, n):
    """
    :param a:
    :param b:
    :param n:
    :return: Whether given parameters are as expected
    """
    if b != a:
        print "Alpha and beta are not consistent"
        return False
    if n % 2 == 1:
        print "N must be even"
        return False
    return True


def get_all_switches(n):
    switches = []
    for top in [True, False]:
        for i in range(n / 2):
            switches.append(Switch(i, n / 2 + i, top))
    return switches


def get_containing_switch(switches, ball, top):
    """
    :param switches:
    :param ball:
    :return: First switch containing the given ball, at any index
    """
    for switch in switches:
        if (switch.left == ball or switch.right == ball) and switch.top == top:
            return switch
    return None


def get_list_of_edges(alpha, beta, n):
    """
    :param alpha:
    :param beta:
    :param n:
    :return: List of edges that should be in the switch graph matching the permutation
    """
    if not validate(len(alpha), len(alpha), n):
        return

    switches = get_all_switches(n)
    edges = []
    for i in range(len(alpha)):
        cross_half = 0
        if (alpha[i] < n / 2 and beta[i] >= n / 2) or (alpha[i] >= n / 2 and beta[i] < n / 2):
            cross_half = 1
        switch1_index = 0 if (alpha[i] < n / 2) else 1
        switch1 = get_containing_switch(switches, alpha[i], True)
        switch2 = get_containing_switch(switches, beta[i], False)
        edges.append(Edge(switch1, switch2, cross_half, switch1_index))
    return edges


def get_switch_neighbours(edges, switch):
    """
    :param edges:
    :param switch:
    :return: All switches that are connected to given switch by an edge
    """
    neighbours = []
    for edge in edges:
        if edge.switches[0] == switch or edge.switches[1] == switch:
            neighbours.append(edge)
    return neighbours


def extend_last_component(components, current_edge, current_switch):
    """
    :param components:
    :param current_edge:
    :param current_switch:
    """
    if current_edge.cross_half:
        components[-1].append([current_edge.switches[current_switch]])
    else:
        components[-1][-1].append(current_edge.switches[current_switch])


def get_white_neighbour(edges, switch, blacklist):
    """
    :param edges:
    :param switch:
    :param blacklist:
    :return: First edge neighbouring the given switch, with a switch not in the blacklist
    """
    neighbours = get_switch_neighbours(edges, switch)
    i = 0
    found_new = False
    while not found_new and i < len(neighbours):
        for j in range(2):
            if blacklist.count(neighbours[i].switches[j]) == 0:
                found_new = True
        i += 1

    if i < len(neighbours):
        return neighbours[i]
    return None


def find_opening_edge(edges, queue):
    """
    :param edges:
    :param queue:
    :return: The first edge in the connected component
    """
    current_switch = 0
    blacklist = []
    next_edge = edges[0]
    while next_edge:
        blacklist.append(next_edge.switches[current_switch])
        current_edge = next_edge
        current_switch = 1 - current_switch
        next_edge = get_white_neighbour(edges, current_edge.switches[current_switch], blacklist)

    queue.append(current_edge)
    edges.remove(current_edge)
    return current_switch


def get_list_of_components(edges):
    """
    :param edges:
    :return:
    """
    components = []
    queue = []
    while len(edges) > 0 or len(queue) > 0:
        if len(queue) == 0:
            current_switch = find_opening_edge(edges, queue)
            start_switch = queue[0].switches[current_switch]
            components.append([[start_switch]])

        current_edge = queue.pop()
        current_switch = 1 - current_switch
        if current_edge.switches[current_switch] != start_switch:
            extend_last_component(components, current_edge, current_switch)
            neighbours = get_switch_neighbours(edges, current_edge.switches[current_switch])
            for neighbour in neighbours:
                edges.remove(neighbour)
                queue.insert(0, neighbour)
    return components


def get_sccs(alpha, beta, n):
    edges = get_list_of_edges(alpha, beta, n)
    return get_list_of_components(edges)
