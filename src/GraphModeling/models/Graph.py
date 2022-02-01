import matplotlib.pyplot as pyplot
import networkx
import numpy

from collections.abc import Sequence, Mapping

class Graph:
    """ The Graph class allows for the generation of directed graphs containing weights and costs.

    members:
        + edges (Sequence): a list of (from, to) node tuples
        + direction_matrix (numpy.ndarray): matrix of the directed edges between nodes
        + networkx_graph (networkx.DiGraph): networkx object representation of graph
    """
    
    def __init__(self, edges: Sequence) -> None:
        """Creates a new instance of the Graph class. Initializes the graph's 
        matricies based on the given general matrix.  

        Args:
            edges (Sequence): a list of edges (node from-to tuples)
        """
        self.edges = edges

        # TODO: initialize connection, weight, and cost matrices using gen_matrix

        # TODO: initialize networkx graph
        self.networkx_graph = networkx.DiGraph()

        
    def print_graph(self) -> None:
        # TODO: Implement
        pass

    def get_simple_paths(self) -> Sequence:
        """Returns an array of simple paths in the graph

        Returns:
            Sequence: a list of paths (a path is an array of nodes)
        """
        # TODO: Implement
        return []

