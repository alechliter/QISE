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
        + node_indicies (Mapping): a dictionary of node indicies to an array of nodes with 
        outgoing edges from that node. Of the form:
            I = { i: [list-of-outgoing-nodes] }
        + treated_node_indicies (Mapping): a dicitionary of node indicies to an array of outgoing
        nodes that have been treated (already touched by the Label Algorithm). Of the form:
            T = { i: [list-of-treated-outgoing-nodes] }
        + node_labels (Mapping): a list of NodeLabl objects, one for each node in the graph
        + source_node (int): index identifier of the source node
        + graph (WCGraph): the weight-constrained graph
    """

    def __init__(self) -> None:
        # TODO: finish
        self.node_indicies: Dict[int, List[int]] = {}
        self.treated_nodes_indicies: Dict[int, List[int]] = {}
        self.node_labels: Dict[int, NodeLabel] = {}
        self.graph: WCGraph
        self.source_node: int
    
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

        # Step 1: Select a label to be treated
        untreated_indicies = self._get_remaining_label_indicies()
        while len(untreated_indicies) != 0:
            # select an untreated node (Look into optimizing this choice later?)
            untreated_indicies = list(untreated_indicies).sort()
            current_node = untreated_indicies[0]
            # Step 2: Treat the label
            pass

    def _initialize_label_setup(self) -> None:
        for node_index in Graph.get_nodes(self.graph.edges):
            # initialize node_indicies
            self.node_indicies[node_index] = self.graph.get_outgoing_nodes(node_index)

            # initialize treated_nodes (initially an empty list for every node)
            self.treated_nodes_indicies[node_index] = []
            
            # initialize node labels
            currentNodeLabel = NodeLabel(node_index, self.graph.get_incoming_nodes(node_index))
            if node_index == self.source_node:
                # the source node as one label: (0, 0)
                currentNodeLabel.add_label(0, 0, node_index)
            self.node_labels[node_index] = currentNodeLabel

        

    def _get_remaining_label_indicies(self) -> Set[int]:
        """
        Returns a set of the union of all label indicies that have not yet been treated: 
            for all i in V: U(I_i - T_i)

        Returns:
            Sequence: a set of all indicies that have not yet been treated.
        """
        remaining_labels: Set = {}

        for node in self.node_indicies.keys():
            if node != self.source_node:
                remaining_labels.union(self._remaining_label_indicies_for_node(node))

        return remaining_labels
    
    def _remaining_label_indicies_for_node(self, node: int) -> Set[int]:
        """
        Returns a list of the remaining indicies not yet treated for a node: I_i - T_i

        Args:
            node (int): the node identifier

        Returns:
            Set[int]: returns a set of node indicies that have not yet been treated for that node
        """
        set_of_indicies = set(self.node_indicies[node])
        set_of_treated = set(self.treated_nodes_indicies[node])
        return set_of_indicies.difference(set_of_treated)