import numpy

from collections.abc import Sequence

from ..models.Graph import Graph

def print_paths(paths: Sequence) -> None:
    for path in paths:
        print(f"|    {path}")

def print_matrix(matrix: numpy.ndarray) -> None:
    for column in matrix:
        print(f"|    {column}")

def main():
    graph = Graph([(0, 1), (1, 2), (1, 3), (3, 4), (2, 4), (4, 5)])

    print("Simple Paths:")
    print_paths(graph.get_simple_paths())

    print("Connection Matrix")
    print_matrix(graph.connection_matrix)

    graph.print_graph()

if __name__ == "__main__":
    main()