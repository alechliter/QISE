import numpy

from collections.abc import Sequence

from ..models.WCGraph import WCGraph

def print_paths(paths: Sequence) -> None:
    for path in paths:
        print(f"|    {path}")

def print_matrix(matrix: numpy.ndarray) -> None:
    for column in matrix:
        print(f"|    {column}")

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

def main():
    graph = WCGraph({
        #edge    constraint
        #s  t    w  c
        (0, 1): (0, 0),
        (1, 2): (5, 6), 
        (1, 3): (2, 3), 
        (3, 4): (4, 4), 
        (2, 4): (5, 9), 
        (4, 5): (8, 7)
        })
    
    test_graph(graph, 20)

    graph_2 = WCGraph({
        #edge    constraint
        #s  t    w  c
        (0, 1): (1, 1),
        (1, 2): (2, 5),
        (0, 3): (1, 1),
        (1, 3): (2, 2),
        (1, 4): (2, 8),
        (2, 4): (1, 2),
        (3, 4): (6, 2),
    })

    test_graph(graph_2, weight = 6)

if __name__ == "__main__":
    main()