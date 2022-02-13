from ctypes import sizeof
import numpy

from collections.abc import Sequence

from ..models.Graph import Graph

import networkx

def main():
    # graphDict = get_maximal_graph(5)
    # # print(graphDict)
    # graph = WCGraph(graphDict)
    # graph.print_graph(suppress_text_output=True)
    
    graphDict2 = arbitrary_graph(5)
    print(graphDict2)
    
    # G = networkx.DiGraph()
    # G.add_edges_from(graphDict2)
    
    graph2 = Graph(graphDict2)
    
    paths = graph2.get_simple_paths()
    print(paths)
    
    graph2.print_graph(suppress_text_output=True)


def get_maximal_graph(n: int) -> dict:
    """Returns a maximal (all paths from s to t) graph

    Args:
        n (int): number of nodes

    Returns:
        dict: returns Graph dictionary with maximum number of edges
    """
    graph = {}
    for i in range(0,n):
        for j in range(i+1,n):
            graph[(i,j)] = (0,0)
    return graph

def arbitrary_graph(n: int) -> dict:
    """Generates arbitrary WCGraph dictionary

    Args:
        n (int): number of nodes

    Returns:
        dict: dictionary of arbitrary WCGraph
    """
    graph = get_maximal_graph(n)
    for i in range(0,n-1):
        num_to_delete = numpy.random.randint(0,n-1-i)
        possible_nodes = [*range(i+1,n-1)]
        for j in range(0, num_to_delete):
            node_to_delete = numpy.random.choice(possible_nodes)
            possible_nodes.remove(node_to_delete)
            graph.pop((i, node_to_delete), None)
    return graph
        
        
def print_paths(paths: Sequence) -> None:
    for path in paths:
        print(f"|    {path}")

def print_matrix(matrix: numpy.ndarray) -> None:
    for column in matrix:
        print(f"|    {column}")

def test_graph(graph: Graph, weight):
    print("Connection Matrix")
    print_matrix(graph.connection_matrix)

    print("Weight Matrix")
    print_matrix(graph.weight_matrix)

    print("Cost Matrix")
    print_matrix(graph.cost_matrix)

    print("Simple Paths:")
    print_paths(graph.get_simple_paths())

    print("Weight Constrained Simple Paths (W = 5):")
    wc_paths = graph.find_wc_paths(weight)
    print_paths(wc_paths)

    print("Lowest Cost Weight Constrained Simple Path (W = 5):")
    path = graph.find_lowest_cost_path(wc_paths)
    print(path)
    print(f"Weight: {graph.calc_path_weight_cost(path)[0]}, Cost: {graph.calc_path_weight_cost(path)[1]}")

    graph.print_graph()
    
if __name__ == "__main__":
    main()