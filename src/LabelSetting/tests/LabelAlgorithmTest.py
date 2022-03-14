
import sys
import networkx
from types import LambdaType
from src.GraphModeling.models.Graph import Graph
from src.GraphModeling.models.WCGraph import WCGraph
from src.LabelSetting.Models.LabelAlgorithmBase import LabelAlgorithmBase

from src.GraphModeling.tests.WCGraphTest import print_graph_details, print_matrix
from src.LabelSetting.Models.LabelAlgorithmIter import LabelAlgorithmIter
from src.LabelSetting.Models.LabelAlgorithmRec import LabelAlgorithmRec
from src.LabelSetting.Models.LabelAlgorithmSpanTree import LabelAlgorithmSpanTree
from src.LabelSetting.Models.SpanningTree import SpanningTree

def print_test_results(graph: WCGraph, labels: LabelAlgorithmBase, destination_node: int):
    for node, label in labels.node_labels.items():
        print(f"|   Labels for node {node}:")
        print(f"|   |   {label.labels}")
        print(f"|   Paths for node {node}: ")
        print(f"|   |   {label.paths}")
        print(f"|   Untreated nodes: {label.get_untreated_nodes()}\n")

    efficient_labels = labels.node_labels[destination_node].get_efficient_labels()
    print(f"|   Efficient labels for the destination node:\n|   |   {efficient_labels}\n")
    print(f"|   Efficient Paths:")
    for node in efficient_labels.keys():
        print(f"|    |   {labels.node_labels[destination_node].paths[node]}")
    
    path = []
    for node in efficient_labels.keys():
        path.extend(labels.node_labels[destination_node].paths[node])
    edges = []
    for i in range(len(path) - 1):
        edges.append((path[i], path[i + 1]))

    print("\ngraph:\n")
        
    graph.print_graph(show_minimal_output = destination_node > 10, highlight_edges = edges)

def print_graph_info(graph: WCGraph, title: str):
    print(f"\n{title}\n")

    print(graph.connection_matrix)
    print(graph.weight_matrix)
    print(graph.cost_matrix)

    for node_index in Graph.get_nodes(graph.edges):
        # find the incoming and outgoing nodes of the current node
        print(f"Incoming Nodes for node {node_index}: {graph.get_incoming_nodes(node_index)}")
        print(f"Outgoing Nodes for node {node_index}: {graph.get_outgoing_nodes(node_index)}")

def test_label_iterative(graph: WCGraph, source_node: int, destination_node: int, weight: int):
    print_graph_info(graph, "Label Algorithm - Iterative")

    labels = LabelAlgorithmIter()

    labels.run_algorithm(graph, source_node, weight)

    print_test_results(graph, labels, destination_node)
    return labels

def test_label_recursive(graph: WCGraph, source_node: int, destination_node: int, weight: int):
    print_graph_info(graph, "Label Algorithm - Recursive")

    labels = LabelAlgorithmRec()

    labels.run_algorithm(graph, source_node, weight)

    print_test_results(graph, labels, destination_node)
    return labels

def test_label_spantree(graph: WCGraph, source_node: int, destination_node: int, weight: int):
    print_graph_info(graph, "Label Algorithm - Spanning Tree")

    labels = LabelAlgorithmSpanTree()

    labels.run_algorithm(graph, source_node, weight)

    print_test_results(graph, labels, destination_node)
    return labels

def test_label_rec_all_labels(graph: WCGraph, source_node: int, destination_node: int, weight: int):
    print_graph_info(graph, "Label Algorithm - Generate all possible labels")

    labels = LabelAlgorithmRec()

    labels.gen_all_possible_labels(graph, source_node, weight)

    print_test_results(graph, labels, destination_node)
    return labels

def test_1_simple_graph_on_all():
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
        (2, 3): (1, 1),
        (3, 5): (2, 3),
        (5, 6): (1, 1)
    })

    test_label_iterative(graph, source_node = 0, destination_node = 6, weight = 6)
    test_label_recursive(graph, source_node = 0, destination_node = 6, weight = 6)
    test_label_spantree(graph, source_node = 0, destination_node = 6, weight = 6)

def test_2_moderate_graph_rec():
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
        (2, 3): (1, 1),
        (3, 5): (2, 3),
        (5, 6): (1, 1),
        (0, 6): (6, 10),
        (4, 5): (1, 1)
    })

    test_label_recursive(graph, source_node = 0, destination_node = 6, weight = 6)

def test_3_moderate_graph_spantree():
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
        (2, 3): (1, 1),
        (3, 5): (2, 3),
        (5, 6): (1, 1),
        (0, 6): (6, 10),
        (4, 5): (1, 1)
    })

    test_label_spantree(graph, source_node = 0, destination_node = 6, weight = 6)

def test_small_graph():
    num_nodes = 5
    graph: WCGraph = WCGraph.get_arbitrary_graph(n = num_nodes, mean_weight = 2, mean_cost = 6)

    try:
        test_label_recursive(graph, source_node = 0, destination_node = num_nodes - 1, weight = 50) 
    except Exception as error:
        graph.save_to_json("LabelAlgorithm_SmallGraph_Crash")
        print(f"Error: {error.__doc__}. Saving graph.")
    except:
        graph.save_to_json("LabelAlgorithm_SmallGraph_UnexpectedCrash")
        print(f"Unexpected error: {sys.exc_info()[0]}")

def test_medium_graph():
    num_nodes = 35
    graph: WCGraph = WCGraph.get_arbitrary_graph(n = num_nodes, mean_weight = 5, mean_cost = 5)

    try:
        test_label_recursive(graph, source_node = 0, destination_node = num_nodes - 1, weight = num_nodes * 10) 
    except Exception as error:
        graph.save_to_json("LabelAlgorithm_MediumGraph_Crash")
        print(f"Error: {error.__doc__}. Saving graph.")
    except:
        graph.save_to_json("LabelAlgorithm_MediumGraph_UnexpectedCrash")
        print(f"Unexpected error: {sys.exc_info()[0]}")

def test_large_graph():
    num_nodes = 50
    graph: WCGraph = WCGraph.get_arbitrary_graph(n = num_nodes, mean_weight = 10, mean_cost = 5)

    try:
        labels = test_label_recursive(graph, source_node = 0, destination_node = num_nodes - 1, weight = num_nodes * 10) 
    except Exception as error:
        graph.save_to_json("LabelAlgorithm_LargeGraph_Crash")
        print(f"Error: {error.__doc__}. Saving graph.")
    except:
        graph.save_to_json("LabelAlgorithm_LargeGraph_UnexpectedCrash")
        print(f"Unexpected error: {sys.exc_info()[0]}")

def test_massive_graph():
    num_nodes = 100
    graph: WCGraph = WCGraph.get_arbitrary_graph(n = num_nodes, mean_weight = 10, mean_cost = 5)
    labels: LabelAlgorithmBase

    try:
        labels = test_label_recursive(graph, source_node = 0, destination_node = num_nodes - 1, weight = num_nodes * 10) 
    except Exception as error:
        graph.save_to_json("LabelAlgorithm_MassiveGraph_Crash")
        print(f"Error: {error.__doc__}. Saving graph.")
    except:
        graph.save_to_json("LabelAlgorithm_MassiveGraph_UnexpectedCrash")
        print(f"Unexpected error: {sys.exc_info()[0]}")


def test_load(graph_name: str, num_nodes: int):
    graph: WCGraph = WCGraph.load_json_graph(graph_name)
    
    try:
        labels = test_label_recursive(graph, source_node = 0, destination_node = num_nodes - 1, weight  = 1000)

    except:
        graph.print_graph(show_minimal_output = True)
        print(f"\n\nnum cycles: {len(list(networkx.simple_cycles(graph.networkx_graph)))}")
        print_matrix(graph.connection_matrix)



def main():
    print("Label Algorithm Test ------------------------------------")

    # Basic graph tests
    # test_1_simple_graph_on_all()
    # test_2_moderate_graph_rec()
    # test_3_moderate_graph_spantree()

    # Small Arbitrary Graph Test
    # test_small_graph()

    # Medium graph test
    # test_medium_graph()

    # Large graph test
    test_large_graph()

    # Massive Graph Test
    # test_massive_graph()

    # Test loaded graph
    # test_load("LabelAlgorithm_LargeGraph_UnexpectedCrash", 50)
    # test_load("LabelAlgorithm_MediumGraph_UnexpectedCrash", 35)
    # test_load("LabelAlgorithm_MassiveGraph_UnexpectedCrash", 100)


if __name__ == "__main__":
    main()