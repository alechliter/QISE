import matplotlib.pyplot as pyplot
import networkx
import numpy

from collections.abc import Sequence

class Graph:
    """ The Graph class allows for the generation of directed graphs containing weights and costs.

    members:
        gen_matrix (numpy.ndarray): general matrix containing weight, cost, and position information in one matrix
        connection_matrix (numpy.ndarray): matrix of the directed edges between nodes
        weight_matrix (numpy.ndarray): matrix of the weights for each edge
        cost_matrix (numpy.ndarray): matrix of the costs for each edge 
        networkx_graph (networkx.DiGraph): networkx object representation of graph
    """
    
    def __init__(self, matrix: numpy.ndarray) -> None:
        """Creates a new instance of the Graph class. Initializes the graph's 
        matricies based on the given general matrix.  

        Args:
            matrix (numpy.ndarray): a general matrix that contains information on the cost 
                and weight for each edge between nodes in the graph.
        """
        self.gen_matrix = matrix

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

