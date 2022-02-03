import numpy

from collections.abc import Sequence, Mapping
from typing import Tuple

from .Graph import Graph

class WCGraph(Graph):
    """Weight-Constrained Graph extends the normal graph, adding functionality specific to 
    the weight-constrained problem.

    members: 
        + weight_matrix (numpy.ndarray): matrix of the weights for each edge
        + cost_matrix (numpy.ndarray): matrix of the costs for each edge
        + wc_edges (Mapping): dictionary of edges to (weight, cost)

    note: this might be useless/overkill for our purposes, we could just add everything to the graph class.
    """

    def __init__(self, edges: Mapping) -> None:
        """Creates a new instance of a Weight-Constrained Graph using a dictionary of edges to weights and costs.

        Args:
            edges (Mapping): a dictionary of edges to their weights and costs {(from, to): (weight, cost)}
        """
        self.wc_edges = edges
        self.weight_matrix: numpy.ndarray
        self.cost_matrix: numpy.ndarray

        # Initialize the base class Graph
        super(WCGraph, self).__init__(edges.keys())

        # Generate Weight and Cost Matricies
        self._generate_weight_cost_matricies()

        pass

    def find_wc_paths(self, weight: int, source_node: int = 0, destination_node: int | None = None) -> Sequence:
        """Creates a list of each path in the graph that follows the weight constraint.

        Args:
            weight (int): the weight constraint for the paths

        Returns:
            Sequence: a list of paths that follow the weight constraint
        """
        wc_paths = []

        for path in self.get_simple_paths(source_node, destination_node):
            path_weight_cost = self.calc_path_weight_cost(path)
            if path_weight_cost[0] <= weight:
                wc_paths.append(path)

        return wc_paths
    
    def find_lowest_cost_path(self, paths: Sequence) -> Sequence:
        """
        Finds the path with the lowest cost given a list of paths.

        Args:
            paths (Sequence): a list of paths (lists of node pairs)

        Returns:
            Sequence: the path with the lowest cost
        """
        lowest_cost_path = []

        if len(paths) > 0:
            lowest_cost_path = paths[0]
            lowest_cost = self.calc_path_weight_cost(paths[0])[1]
            for path in paths:
                path_weight_cost = self.calc_path_weight_cost(path)
                if path_weight_cost[1] < lowest_cost:
                    lowest_cost_path = path
                    lowest_cost = path_weight_cost[1]

        return lowest_cost_path

    def calc_path_weight_cost(self, path: Sequence) -> Tuple:
        """calculates the total weight and cost along a given path

        Args:
            path (Sequence): the path of nodes (an array of nodes in order of path traversal)

        Returns:
            Sequence: the total [weight, cost] along the path
        """
        total_weight = 0
        total_cost = 0

        for index in range(len(path) - 1):
            edge = (path[index], path[index + 1])
            total_weight += self.wc_edges[edge][0] # weight
            total_cost += self.wc_edges[edge][1] # cost

        return (total_weight, total_cost)

    def print_graph(self, picture_name: str = "") -> None:
        """
        Prints the graph with (weight, cost) labels for each edge

        Args:
            picture_name (str, optional): The name of the file to save the picture to. Defaults to "".
        """
        edge_labels = {}

        for edge, constraints in self.wc_edges.items():
            edge_labels[edge] = f"{constraints[0]}, {constraints[1]}"

        super(WCGraph, self).print_graph(picture_name, edge_labels)

    def _generate_weight_cost_matricies(self):
        """
        Generates the weight and cost matrices based on the weights and costs associated with each pair
        in the dictionary wc_edges
        """
        # initialize matrix to nxn 0 matrix
        self.weight_matrix = Graph._gen_zero_n_square_matrix(self.edges)
        self.cost_matrix = Graph._gen_zero_n_square_matrix(self.edges)

        for edge, constraints in self.wc_edges.items():
            self.weight_matrix[edge[0] - 1][edge[1] - 1] = constraints[0]
            self.cost_matrix[edge[0] - 1][edge[1] - 1] = constraints[1]