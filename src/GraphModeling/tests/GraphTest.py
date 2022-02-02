from collections.abc import Sequence
from ..models.Graph import Graph

def print_paths(paths: Sequence) -> None:
    for path in paths:
        print(path)

def main():
    graph = Graph([(1, 2), (1, 3), (3, 4)])

    print_paths(graph.get_simple_paths())

    graph.print_graph()

if __name__ == "__main__":
    main()