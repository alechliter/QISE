from ctypes import sizeof
import numpy
from numpy import random as r

from collections.abc import Sequence

from ..models.Graph import Graph
from ..models.WCGraph import WCGraph

import networkx

def main():
    # for i in range(1,6):
    graph = WCGraph.get_arbitrary_graph(30,5,3,std_weight=2, peak=10)
    graph.print_graph(picture_name = f"resources/ArbitraryGraphTestResults/TEST", show_minimal_output=True)
        # print(f"Paths of the graph {i}")
        # print_paths(graph.get_simple_paths())
        # print(f"Nodes in the graph: {WCGraph.get_nodes(graph.edges)}")
        # # graph.print_graph()
        # graph.print_graph(picture_name = f"resources/ArbitraryGraphTestResults/arb5graph_{i}", suppress_text_output=True)
    

def get_random_weight_cost(mean_weight: int, mean_cost: int, std_weight:int=1, std_cost:int=1):
    """Generates a random cost-weight tuple based on input. Currently normal dist, but could test with other modes

    Args:
        mean_weight (int): mean weight in normal distribution
        mean_cost (int): mean cost in normal distribution
        std_weight (int, optional): standard deviation of weight. Defaults to 1.
        std_cost (int, optional): standard deviation of cost. Defaults to 1.

    Returns:
        _type_: random weight-cost tuple integers
    """    
    #choose random cost and weight (normal)
    random_weight = int(max(numpy.floor(r.normal(mean_weight,std_weight)),1))
    random_cost = int(max(numpy.floor(r.normal(mean_cost,std_cost)),1))
    
    return (random_weight,random_cost)

def get_arbitrary_graph(n: int, mean_weight: int, mean_cost: int, std_weight:int=1, std_cost:int=1, peak: int=5) -> Graph:
    """Generates arbitrary WC graph with n nodes with normally distributed weights and costs

    Args:
        n (int): number of nodes
        mean_weight (int): mean weight
        mean_cost (int): mean cost
        std_weight (int): standard deviation of weight
        std_cost (int): standard deviation of cost
        peak (int): max number of nodes ahead a node can have an edge to

    Returns:
        Graph: arbitary WC graph with (w,c) normally distributed
    """
    graphDict = {}
    #Loop i range(0,n-1)
    for i in range(0,n-1):
        #Random Noe range(i,n-i) # of outgoing edge
        #TODO: Adjust number of outgoing nodes so you don't go over for peaking
        n_forward = min(n-i-1, peak)
        N_oe = r.randint(1,n_forward+1) if n_forward > 1 else 1 #num outgoing edges
        # print([n_forward,N_oe])
        print("i:", i, "\tn_forward:", n_forward, "\tN_oe:", N_oe)
        #Choose Noe unique nodes range(1,n) delta_o[]
        #TODO: Peaking variable happens here
        delta_o = r.choice([*range(i+1,min(n-1,i+peak)+1)], N_oe, replace=False) if i!=n-1 else [n]
        #For each j in delta_o[], add edge (i,j)
        for j in delta_o:
            graphDict[i,j] = get_random_weight_cost(mean_weight, mean_cost, std_weight=std_weight, std_cost=std_cost)
        #If no incoming nodes
        oneInNode = False
        for k in range(0,i):
            if((k,i) in graphDict):
                oneInNode = True
                break
        if not oneInNode and i != 0:
            #TODO: Adjust range to fit peaking variable
            #Choose node incoming n_in range(0,i-1)
            n_in = r.randint(max(0,i-peak),i-1) if i>1 else 0
            #Add edge (n_in,i)
            graphDict[n_in,i] = get_random_weight_cost(mean_weight, mean_cost, std_weight=std_weight, std_cost=std_cost)
        
    graph = WCGraph(graphDict)
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