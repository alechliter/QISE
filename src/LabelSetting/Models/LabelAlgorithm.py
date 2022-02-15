from typing import Dict, List, Set

from ...GraphModeling.models.WCGraph import WCGraph
from ...GraphModeling.models.Graph import Graph
from .NodeLabel import NodeLabel

class LabelAlgorithm:
    """
    The LabelAlgorithm class defines an object that keeps track of the NodeLabels for each 
    node in a weight-constrained graph, applying the Label Setting Algorithm defined in the
    paper "Algorithms for the weight constrained shortest path problem" by Irina Dumitrescu
    and Natashia Boland.

    members:
        + node_labels (Dict[int, NodeLabel]): a list of NodeLabl objects, one for each node in the graph
        + source_node (int): index identifier of the source node
        + graph (WCGraph): the weight-constrained graph
    """

    def __init__(self) -> None:
        self.node_labels: Dict[int, NodeLabel] = {}
        self.graph: WCGraph = None
        self.source_node: int = None
    
    def run_algorithm(self, graph: WCGraph, source_node: int):
        """
        Runs the Label Setting Algorithm on the given weight-constrained graph with the given source node.

        Args:
            graph (WCGraph): the weight-constrained graph
            source_node (int): the index that defines the source node
        """
        # TODO: finish
        self.graph = graph
        self.source_node = source_node

        # Step 0: Initialize the labels
        self._initialize_label_setup()

        # Step 1a: Select a label to be treated
        untreated_indicies = self._get_remaining_label_indicies()
        while len(untreated_indicies) != 0:
            current_node = self._get_next_node()
            i = current_node.node_index
            if current_node:
                # Step 1b: select an untreated index of the node such that the total weight is minimal
                #   meaning: given node i, select node index k from the list of untreated incoming nodes to i such 
                #            that the weight of the edge (k, i) is the smallest among incoming edges to i
                untreated_in_nodes = current_node.get_untreated_nodes()
                k_in = None
                for j_in in untreated_in_nodes:
                    if not k_in:
                        W_k_i = self.graph.edges[k_in, i][0] # the weight of edge (k, i)
                        W_j_i = self.graph.edges[j_in, i][0] # the weight of edge (j, i)
                        if W_j_i < W_k_i:
                            k_in = j_in
                    else:
                        k_in = j_in
                # TODO: Step 2: Treat the label
            else:
                print("Error: untreated nodes remain yet no next node found")
                break
            

    def _initialize_label_setup(self) -> None:
        for node_index in Graph.get_nodes(self.graph.edges):
            # find the incoming and outgoing nodes of the current node
            incoming_nodes = self.graph.get_incoming_nodes(node_index)
            outgoing_nodes = self.graph.get_outgoing_nodes(node_index)

            # initialize node label
            currentNodeLabel = NodeLabel(node_index, incoming_nodes, outgoing_nodes)
            if node_index == self.source_node:
                # the source node as one label: (0, 0)
                currentNodeLabel.add_label(0, 0, node_index)
            self.node_labels[node_index] = currentNodeLabel    

    def _get_remaining_label_indicies(self) -> Set[int]:
        """
        Returns a set of the union of all label indicies that have not yet been treated: 
            for all i in V: U(I_i - T_i)

        Returns:
            Set[int]: a set of all indicies that have not yet been treated.
        """
        remaining_labels: Set[int] = {}

        for node, node_label in self.node_labels.items():
            if node != self.source_node:
                remaining_labels.union(node_label.get_untreated_nodes())

        return remaining_labels
    
    def _get_next_node(self) -> NodeLabel | None:
        """
        Gets the next node with untreated incoming node-labels

        Returns:
            [NodeLabel | None]: returns either the next node if one exists or None.
        """
        next_node: NodeLabel | None = None

        for node in self.node_labels.values():
            if node.node_index != self.source_node and len(node.get_untreated_nodes) != 0:
                next_node = node
                break

        return next_node