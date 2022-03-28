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
    x = [(0, 29), (29, 50), (50, 99), (0, 41), (41, 51), (51, 99), (0, 36), (36, 37), (37, 54), (54, 99), (0, 33), (33, 59), (59, 99), (0, 5), (5, 23), (23, 24), (24, 60), (60, 99), (36, 64), (64, 99), (59, 68), (68, 99), (0, 47), (47, 69), (69, 99), (0, 30), (30, 70), (70, 99), (36, 75), (75, 99), (33, 56), (56, 76), (76, 99), (36, 63), (63, 79), (79, 99), (63, 81), (81, 99), (75, 85), (85, 99), (47, 88), (88, 99), (47, 91), (91, 99), (64, 98), (98, 99)]
    graph = Graph(x)

    print("Simple Paths:")
    print_paths(graph.get_simple_paths())

    print("Connection Matrix")
    print_matrix(graph.connection_matrix)

    # graph.print_graph()

if __name__ == "__main__":
    main()