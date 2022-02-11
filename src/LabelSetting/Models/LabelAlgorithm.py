from collections.abc import Sequence, Mapping

from ...GraphModeling.models.WCGraph import WCGraph

class LabelAlgorithm:
    """
    The LabelAlgorithm class defines an object that keeps track of the NodeLabels for each 
    node in a weight-constrained graph, applying the Label Setting Algorithm defined in the
    paper "Algorithms for the weight constrained shortest path problem" by Irina Dumitrescu
    and Natashia Boland.

    members:
        + node_indicies (Mapping): a dictionary of node indicies to an array of nodes with 
        outgoing edges to that node. Of the form:
            I = { i: [list-of-incoming-nodes] }
        + treated_node_indicies (Mapping): a dicitionary of node indicies to an array of incoming
        nodes that have been treated (already touched by the Label Algorithm). Of the form:
            T = { i: [list-of-treated-incoming-nodes] }
        + source_node (int): index identifier of the source node
        + graph (WCGraph): the weight-constrained graph
    """

    def __init__(self) -> None:
        # TODO: finish
        self.node_indicies = {}
        self.treated_nodes_indicies = {}
        self.graph: WCGraph
        self.source_node: int
    
    def run_algorithm(self, graph: WCGraph, source_node: int):
        """
        Runs the Label Setting Algorithm on the given weight-constrained graph with the given source node.

        Args:
            graph (WCGraph): the weight-constrained graph
            source_node (int): the index that defines the source node
        """
        # TODO: implement
        self.graph = graph
        self.source_node = source_node

        # Step 0: Initialize the labels
        self._initialize_label_setup()



        # Step 1: Select a label to be treated
        
            # Step 2: Treat the label

        pass

    def _initialize_label_setup(self) -> None:
        # TODO: implement
        pass

    def _get_remaining_label_indicies(self) -> Sequence:
        """
        Returns a list of the union of all label indicies that have not yet been treated.

        Returns:
            Sequence: a list of all indicies that have not yet been treated.
        """
        #TODO: implement
        return []