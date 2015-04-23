from core.graph import Edge, Switch


def calculate_benes(alpha, beta, n):
	"""
	Calculate the probability of an ordered set alpha to get to the ordered set beta
	with n being the current size of the net
	"""
	edges = get_list_of_edges(alpha, beta, n)
	switches = get_switches(edges)
	sccs = get_sccs(edges, switches)


def get_list_of_edges(alpha, beta, n):
	s1 = Switch(0, 4)
	s2 = Switch(1, 5)
	s3 = Switch(2, 6)
	s4 = Switch(3, 7)
	e1 = Edge(s1, s3, 1, 1)
	e2 = Edge(s2, s3, 0, 1)
	e3 = Edge(s4, s4, 0, 1)
	e4 = Edge(s4, s4, 1, 1)

	return [e1, e2, e3, e4]


def get_sccs(edges, switches):
	"""
	Return a list of all the strongly connected components in the graph.
	Each element of the list points to a list of switches that are a part of a sccs.
	"""
	sccs = []

	return sccs


def get_switches(edges):
	"""
	Return all the switches that appear in the edges
	"""
	switches = set()
	for edge in edges:
		switches.add(edge.switch1)
		switches.add(edge.switch2)

	return switches