from search import *
from myutils import *
from GraphProblem import *
import timeit

def breadth_first_graph_search(problem):
	nodes_visited = 1
	node = Node(problem.initial)

	if problem.goal_test(node.state):
		return node

	frontier = deque([node])
	explored = set()

	while frontier:
		node = frontier.popleft()
		explored.add(node.state)

		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				nodes_visited += 1
				if problem.goal_test(child.state):
					return (child, nodes_visited)

				frontier.append(child)
	return None

def depth_first_graph_search(problem):
	nodes_visited = 0

	frontier = [(Node(problem.initial))]
	explored = set()

	while frontier:
		node = frontier.pop()

		nodes_visited += 1
		if problem.goal_test(node.state):
			return (node, nodes_visited)

		explored.add(node.state)
		frontier.extend(child for child in node.expand(problem)
						if child.state not in explored and
						child not in frontier)

	return None

def sorted_depth_first_graph_search(problem):
	nodes_visited = 0

	frontier = [(Node(problem.initial))]
	explored = set()

	while frontier:
		node = frontier.pop()

		nodes_visited += 1
		if problem.goal_test(node.state):
			return (node, nodes_visited)

		explored.add(node.state)
		frontier.extend(child for child in sorted(node.expand(problem))
						if child.state not in explored and
						child not in frontier)

	return None

def best_first_graph_search(problem, f):
	nodes_visited = 0
	f = memoize(f, 'f')
	node = Node(problem.initial)
	frontier = PriorityQueue('min', f)

	frontier.append(node)

	explored = set()

	while frontier:
		node = frontier.pop()

		nodes_visited += 1
		if problem.goal_test(node.state):
			return (node, nodes_visited)

		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				frontier.append(child)

			elif child in frontier:
				if f(child) < frontier[child]:
					del frontier[child]
					frontier.append(child)
	return None

def solve_bfs(graph, initial = '50x10', goal = '10x50'):
	prob = GraphProblem(initial, goal, graph);

	final_node, nodes_visited = breadth_first_graph_search(prob)
	return (get_full_solution(final_node), nodes_visited)

def solve_dfs(graph, initial = '50x10', goal = '10x50'):
	prob = GraphProblem(initial, goal, graph);

	final_node, nodes_visited = depth_first_graph_search(prob)
	return (get_full_solution(final_node), nodes_visited)

def solve_sdfs(graph, initial = '50x10', goal = '10x50'):
	prob = GraphProblem(initial, goal, graph);

	final_node, nodes_visited = sorted_depth_first_graph_search(prob)
	return (get_full_solution(final_node), nodes_visited)

def solve_gbfs(graph, initial = '50x10', goal = '10x50', h = None):
	prob = GraphProblem(initial, goal, graph);

	h = memoize(h or prob.h, 'h')
	final_node, nodes_visited = best_first_graph_search(prob, lambda n: h(n))
	return (get_full_solution(final_node), nodes_visited)

def solve_astar(graph, initial = '50x10', goal = '10x50', h = None):
	prob = GraphProblem(initial, goal, graph);

	h = memoize(h or prob.h, 'h')
	final_node, nodes_visited = best_first_graph_search(prob, lambda n: n.path_cost + h(n))
	return (get_full_solution(final_node), nodes_visited)

for sol in [solve_bfs, solve_dfs, solve_sdfs, solve_gbfs, solve_astar]:
	fn_name = sol.__name__

	print('#{0}'.format(fn_name))

	print(timeit.timeit('{0}(graph)'.format(fn_name), setup = 'from __main__ import {0}; from myutils import build_graph; graph = build_graph();'.format(fn_name), number = 100) / 100)
