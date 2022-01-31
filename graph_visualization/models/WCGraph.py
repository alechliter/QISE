from collections.abc import Sequence

from .Graph import Graph

class WCGraph(Graph):
    """Weight-Constrained Graph extends the normal graph, adding functionality specific to 
    the weight-constrained problem.

    note: this might be useless/overkill for our purposes, we could just add everything to the graph class.
    """

    def __init__(self) -> None:
        # TODO: implement
        pass

    def find_wc_paths(self, weight: float) -> Sequence:
        """Creates a list of each path in the graph that follows the weight constraint.

        Args:
            weight (float): the weight constraint for the paths

        Returns:
            Sequence: a list of paths that follow the weight constraint
        """
        # TODO: implement
        return []

    def calc_path_cost(self, path: Sequence) -> float:
        """calculates the total cost along a given path

        Args:
            path (Sequence): the path of nodes (an array of nodes in order of path traversal)

        Returns:
            float: the total cost along the path
        """
        # TODO: implement
        return 0.0

    def calc_path_weight(self, path: Sequence) -> float:
        """calculates the total weight along a given path

        Args:
            path (Sequence): the path of nodes (an array of nodes in order of path traversal)

        Returns:
            float: the total weight along the path
        """
        # TODO: implement
        return 0.0
