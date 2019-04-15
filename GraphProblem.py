from search import *
from utils import distance_squared

class GraphProblem(Problem):
	"""The problem of searching a graph from one node to another."""

	def __init__(self, initial, goal, graph):
		Problem.__init__(self, initial, goal)
		self.graph = graph

	def actions(self, A):
		"""The actions at a graph node are just its neighbors."""
		return list(self.graph.get(A).keys())

	def result(self, state, action):
		"""The result of going to a neighbor is just that neighbor."""
		return action

	def path_cost(self, cost_so_far, A, action, B):
		return cost_so_far + (self.graph.get(A, B) or infinity)

	def find_min_edge(self):
		"""Find minimum value of edges."""
		m = infinity
		for d in self.graph.graph_dict.values():
			local_min = min(d.values())
			m = min(m, local_min)

		return m

	def h(self, node):
		#print(node)
		"""h function is straight-line distance from a node's state to goal."""
		locs = getattr(self.graph, 'locations', None)
		if locs:
			if type(node) is str:
				return int(distance_squared(locs[node], locs[self.goal]))

			return int(distance_squared(locs[node.state], locs[self.goal]))
		else:
			return infinity
