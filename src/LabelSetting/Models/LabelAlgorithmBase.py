from typing import Dict, Set

from ...GraphModeling.models.WCGraph import WCGraph
from ...GraphModeling.models.Graph import Graph
from .NodeLabel import NodeLabel

class LabelAlgorithmBase:
    """
    The LabelAlgorithm class defines an object that keeps track of the NodeLabels for each 
    node in a weight-constrained graph, applying the Label Setting Algorithm defined in the
    paper "Algorithms for the weight constrained shortest path problem" by Irina Dumitrescu
    and Natashia Boland.

    v1 - calculates the paths from the source to the node for EVERY node in the graph. Inefficient but acccurate

    members:
        + node_labels (Dict[int, NodeLabel]): a list of NodeLabl objects, one for each node in the graph
        + source_node (int): index identifier of the source node
        + graph (WCGraph): the weight-constrained graph
    """

    def __init__(self) -> None:
        self.node_labels: Dict[int, NodeLabel] = {}
        self.graph: WCGraph = None
        self.source_node: int = None
        self.max_weight: int = None

    def _initialize_label_setup(self) -> None:
        for node_index in self.graph.nodes:
            # find the incoming and outgoing nodes of the current node
            incoming_nodes = self.graph.get_incoming_nodes(node_index)
            outgoing_nodes = self.graph.get_outgoing_nodes(node_index)

            # initialize node label
            currentNodeLabel = NodeLabel(node_index, incoming_nodes, outgoing_nodes)
            if node_index == self.source_node:
                # the source node as one label: (0, 0)
                currentNodeLabel.add_label(0, 0, node_index)
                currentNodeLabel.add_path([], 0)
            self.node_labels[node_index] = currentNodeLabel    

    def _get_remaining_label_indicies(self) -> Set[int]:
        """
        Returns a set of the union of all label indicies that have not yet been treated: 
            for all i in V: U(I_i - T_i)

        Returns:
            Set[int]: a set of all indicies that have not yet been treated.
        """
        remaining_labels: Set[int] = set()

        for node, node_label in self.node_labels.items():
            if node != self.source_node:
                # union of the remaining labels with the current node's untreated labels
                remaining_labels.update(node_label.get_untreated_nodes())
        return remaining_labels

