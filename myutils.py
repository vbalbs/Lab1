from search import *
from sys import setrecursionlimit

WALL_TILE = 1
EMPTY_TILE = 0

setrecursionlimit(10000)

def build_grid_row(r):
	left_wall = int(r > 20)
	right_wall = int(r <= 40)

	# the grid is 61x61
	if (r == 0 or r == 60):
		return [WALL_TILE] * 61
	else:
		return [WALL_TILE] + ([EMPTY_TILE] * 19) + [left_wall] + ([EMPTY_TILE] * 19) + [right_wall] + ([EMPTY_TILE] * 19) + [WALL_TILE]

def get_node_name(x, y):
	return '{0:0>2}x{1:0>2}'.format(x, y)

def build_graph():
	grid = [build_grid_row(r) for r in range(0, 61)]
	locations = {}
	dict_graph = {}

	for x in range(61):
		for y in range(61):
			locations[get_node_name(x, y)] = (x, 60 - y)

			if (grid[y][x] == WALL_TILE):
				continue;

			valid_neighbors = {}
			for xx in range(x - 1, x + 2):
				for yy in range(y - 1, y + 2):
					if (xx < 0 or xx > 60 or yy < 0 or yy > 60):
						continue;

					if (xx == x and yy == y):
						continue;

					if (grid[yy][xx] == WALL_TILE):
						continue;

					valid_neighbors[get_node_name(xx, yy)] = 1

			dict_graph[get_node_name(x, y)] = valid_neighbors

	graph = UndirectedGraph(dict_graph)
	graph.locations = locations

	return graph

def get_full_solution(final_node):
	if (not final_node.parent):
		return [final_node.state];

	return [final_node.state] + get_full_solution(final_node.parent)
