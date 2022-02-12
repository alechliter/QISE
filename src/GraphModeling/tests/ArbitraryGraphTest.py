import numpy

from collections.abc import Sequence

from ..models.WCGraph import WCGraph

def main():
    graphDict = set_maximal_graph(20)
    print(graphDict)
    graph = WCGraph(graphDict)
    graph.print_graph(suppress_text_output=True)

#returns a maximal (all paths from s to t) graph
def set_maximal_graph(n: int) -> dict:
    graph = {}
    for i in range(0,n):
        for j in range(i+1,n):
            graph[(i,j)] = (0,0)
    return graph

def print_paths(paths: Sequence) -> None:
    for path in paths:
        print(f"|    {path}")

def print_matrix(matrix: numpy.ndarray) -> None:
    for column in matrix:
        print(f"|    {column}")

def print_graph(graph: WCGraph):
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

def test_graph(graph: WCGraph, weight):
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