from collections.abc import Sequence, Mapping

from .Graph import Graph

class WCGraph(Graph):
    """Weight-Constrained Graph extends the normal graph, adding functionality specific to 
    the weight-constrained problem.

    members: 
        + weight_matrix (numpy.ndarray): matrix of the weights for each edge
        + cost_matrix (numpy.ndarray): matrix of the costs for each edge 

    note: this might be useless/overkill for our purposes, we could just add everything to the graph class.
    """

    def __init__(self, edges: Mapping) -> None:
        """Creates a new instance of a Weight-Constrained Graph using a dictionary of edges to weights and costs.

        Args:
            edges (Mapping): a dictionary of edges to their weights and costs {(from, to): (weight, cost)}
        """
        # TODO: implement
        pass

    def find_wc_paths(self, weight: int) -> Sequence:
        """Creates a list of each path in the graph that follows the weight constraint.

        Args:
            weight  int): the weight constraint for the paths

        Returns:
            Sequence: a list of paths that follow the weight constraint
        """
        # TODO: implement
        return []

    def calc_path_cost(self, path: Sequence) -> int:
        """calculates the total cost along a given path

        Args:
            path (Sequence): the path of nodes (an array of nodes in order of path traversal)

        Returns:
         int: the total cost along the path
        """
        # TODO: implement
        return 0.0

    def calc_path_weight(self, path: Sequence) -> int:
        """calculates the total weight along a given path

        Args:
            path (Sequence): the path of nodes (an array of nodes in order of path traversal)

        Returns:
         int: the total weight along the path
        """
        # TODO: implement
        return 0.0
