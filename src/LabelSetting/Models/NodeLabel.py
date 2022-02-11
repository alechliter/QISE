from collections.abc import Sequence, Mapping

class NodeLabel:
    """
    The Node Label class defines a label-storing object for a node in a weight-constrained graph.
        
    members:
        + node_index (int): the index identifier of the node
        + labels (Mapping): a dictionary of node indicies to labels, of the form:
            L_i = { j : (W_jk + w_ji, C_jk + c_ji) }
        + incoming_nodes (Sequence): a list of indicies of nodes with outgoing edges to this node.
    """

    def __init__(self, index: int) -> None:
        # TODO: finish
        self.node_index = index
        self.labels: Mapping = {}
        self.incoming_nodes = []

    def add_label(self, weight: int, cost: int, index: int) -> None:
        """
        Adds a label to the list of labels for the node.

        Args:
            weight (int): the total weight of the label
            cost (int): the total cost of the label
            index (int): the index of the node where the edge came from
        """
        # TODO: implement
        pass

    def is_label_dominated(self, weight: int, cost: int) -> bool:
        """
        Checks if a label is dominated based on the weight and cost. A label is dominated if
        its weight and cost are both less than the weight and cost of another node in the set
        of labels for this node. 

        Args:
            weight (int): [description]
            cost (int): [description]

        Returns:
            bool: [description]
        """
        # TODO: implement
        pass

    def get_efficient_labels(self) -> Sequence:
        """
        Returns a list of all the efficient labels for the node. An efficient label is a label
        that is not dominated by any other label for the node.

        Returns:
            Sequence: [description]
        """
        # TODO: implement
        pass
    
