import itertools
import math

class Node:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.n = n

def calculate_distance(node1, node2):
    # Calculate the Euclidean distance between two nodes
    return math.sqrt((node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2)

def tsp_subset_nearest_neighbor(nodes, n, start_node):
    subsets = itertools.combinations(nodes, n)

    shortest_path = None
    shortest_distance = float('inf')

    for subset in subsets:
        path = [start_node]
        unvisited = set(subset)
        if start_node in unvisited:
            unvisited.remove(start_node)

        current_node = start_node
        while unvisited:
            nearest_node = min(unvisited, key=lambda node: calculate_distance(current_node, node))
            path.append(nearest_node)
            unvisited.remove(nearest_node)
            current_node = nearest_node

        total_distance = sum(calculate_distance(path[i], path[i + 1]) for i in range(len(path) - 1))

        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_path = path

    return shortest_path, shortest_distance

# The total set of nodes
nodes = [
    Node(84, 1166, 1),
    Node(317, 882, 2),
    Node(558, 890, 3),
    Node(990, 874, 4),
    Node(674, 570, 5),
    Node(656, 460, 6),
    Node(763, 340, 7),
    Node(684, 116, 8),
    Node(568, 126, 9),
    Node(512, 2, 10),
    Node(328, 100, 11),
    Node(350, 184, 12),
    Node(14, 267, 13),
    Node(4, 516, 14),
    Node(281, 528, 15)
] 

# Number of nodes to visit
n = 10  

# Starting node
start_node = nodes[0]

shortest_path, shortest_distance = tsp_subset_nearest_neighbor(nodes, n, start_node)

print("Shortest Path:")
for node in shortest_path:
    print(f"({node.x}, {node.y}, number: {node.n})")

print("Shortest Distance:", shortest_distance)
