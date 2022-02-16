from src.GraphModeling.models.Graph import Graph
from src.GraphModeling.models.WCGraph import WCGraph
from src.LabelSetting.Models.LabelAlgorithm import LabelAlgorithm

def test_graph_v1(graph: WCGraph, source_node: int, destination_node: int, weight: int):
    print("\nLabel Algorithm v1\n")
    labels = LabelAlgorithm()

    print(graph.connection_matrix)

    for node_index in Graph.get_nodes(graph.edges):
        # find the incoming and outgoing nodes of the current node
        print(f"Incoming Nodes for node {node_index}: {graph.get_incoming_nodes(node_index)}")
        print(f"Outgoing Nodes for node {node_index}: {graph.get_outgoing_nodes(node_index)}")

    labels.run_algorithm_v1(graph, source_node, weight)

    for node, label in labels.node_labels.items():
        print(f"|   Labels for node {node}:")
        print(f"|   |   {label.labels}")
        print(f"|   Untreated nodes: {label.get_untreated_nodes()}")

    efficient_labels = labels.node_labels[destination_node].get_efficient_labels()
    print(f"|   Efficient labels for the destination node:\n|  |   {efficient_labels}")

def test_graph_v2(graph: WCGraph, source_node: int, destination_node: int, weight: int):
    print("\nLabel Algorithm v2\n")
    labels = LabelAlgorithm()

    print(graph.connection_matrix)

    for node_index in Graph.get_nodes(graph.edges):
        # find the incoming and outgoing nodes of the current node
        print(f"Incoming Nodes for node {node_index}: {graph.get_incoming_nodes(node_index)}")
        print(f"Outgoing Nodes for node {node_index}: {graph.get_outgoing_nodes(node_index)}")

    labels.run_algorithm_v2(graph, source_node, weight)

    for node, label in labels.node_labels.items():
        print(f"|   Labels for node {node}:")
        print(f"|   |   {label.labels}")
        print(f"|   Untreated nodes: {label.get_untreated_nodes()}")

    efficient_labels = labels.node_labels[destination_node].get_efficient_labels()
    print(f"|   Efficient labels for the destination node:\n|  |   {efficient_labels}")

def main():
    print("Label Algorithm Test ------------------------------------")

    graph = WCGraph({
        #edge    constraint
        #s  t    w  c
        (0, 1): (1, 1),
        (1, 2): (2, 5),
        (0, 3): (1, 1),
        (1, 3): (2, 2),
        (1, 4): (2, 8),
        (2, 4): (7, 2),
        (3, 4): (6, 2),
        (0, 2): (0, 1),
        (2, 3): (1, 1)
    })

    test_graph_v1(graph, source_node = 0, destination_node = 4, weight = 6)
    test_graph_v2(graph, source_node = 0, destination_node = 4, weight = 6)

    print("\ngraph:\n")

    graph.print_graph()

if __name__ == "__main__":
    main()