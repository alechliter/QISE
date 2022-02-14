from ctypes import sizeof
import numpy
from numpy import random as r

from collections.abc import Sequence

from ..models.Graph import Graph

import networkx

def main():
    for i in range(1,11):
        graph = get_arbitrary_graph(5)
        print(f"Paths of the graph {i}")
        print_paths(graph.get_simple_paths())
        print(f"Nodes in the graph: {Graph.get_nodes(graph.edges)}")
        graph.print_graph(picture_name = f"resources/ArbitraryGraphTestResults/arb5graph_{i}", suppress_text_output=True)
    

def get_arbitrary_graph(n: int) -> Graph:
    """Generates arbitrary WC graph with n nodes and no weights or costs

    Args:
        n (int): number of nodes

    Returns:
        Graph: arbitary WC graph with all (w,c) = (0,0)
    """
    graphDict = {}
    #Loop i range(0,n)
    for i in range(0,n-1):
        #Random Noe range(i,n) # of outgoing edges
        N_oe = r.randint(1,n-i) if n-i>1 else 1
        #print("i :", i, "\tN_oe: ", N_oe)
        #Choose Noe unique nodes range(1,n) delta_o[]
        delta_o = r.choice([*range(i+1,n)], N_oe, replace=False) if i!=n-1 else [n]
        #For each j in delta_o[], add edge (i,j)
        for j in delta_o:
            #TODO: Add weights and cost generation
            graphDict[i,j] = (0,0)
        #If no incoming nodes
        oneInNode = False
        for k in range(0,i):
            if((k,i) in graphDict):
                oneInNode = True
                break
        if not oneInNode and i != 0:
            #Choose node incoming n_in range(0,i-1)
            n_in = r.randint(0,i-1) if i>1 else 0
            #Add edge (n_in,i)
            #TODO: Add weight and const
            graphDict[n_in,i] = (0,0)
        
    graph = Graph(graphDict)
    return graph

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