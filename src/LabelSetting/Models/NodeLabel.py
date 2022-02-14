
from typing import Dict, List, Tuple


class NodeLabel:
    """
    The Node Label class defines a label-storing object for a node in a weight-constrained graph.
        
    members:
        + node_index (int): the index identifier of the node
        + labels (Dict[int, Tuple(int, int)]): a dictionary of node indicies to labels, of the form:
            L_i = { j : (W_jk + w_ji, C_jk + c_ji) }
        + incoming_nodes (Sequence): a list of indicies of nodes with outgoing edges to this node.
    """

    def __init__(self, index: int, incoming_nodes: List[int] = []) -> None:
        """
        Creates a new instance of a NodeLabel object.

        Args:
            index (int): the index identifier of the node
            incoming_nodes (List[int], optional): the list of nodes with outgoing edges going to the node. Defaults to [].
        """
        self.node_index = index
        self.incoming_nodes = incoming_nodes
        self.labels: Dict[int, Tuple[int, int]] = { node: [] for node in incoming_nodes }

    def add_label(self, weight: int, cost: int, index: int) -> None:
        """
        Adds a label to the list of labels for the node.

        Args:
            weight (int): the total weight of the label
            cost (int): the total cost of the label
            index (int): the index of the node where the edge came from
        """
        if index not in self.incoming_nodes:
            self.incoming_nodes.append(index)
        
        self.labels[index] = (weight, cost)

    def is_label_dominated(self, weight: int, cost: int) -> bool:
        """
        Checks if a label is dominated based on the weight and cost. A label is dominated if
        its weight and cost are both less than the weight and cost of another node in the set
        of labels for this node. 

        Args:
            weight (int): the weight of the label
            cost (int): the cost of the label

        Returns:
            bool: true if the label is dominated by at least one label in this node
        """

        return NodeLabel._is_label_dominated_in_list(weight, cost, self.labels.value())

    def get_efficient_labels(self) -> Dict[int, Tuple[int, int]]:
        """
        Returns a list of all the efficient labels for the node. An efficient label is a label
        that is not dominated by any other label for the node.

        Returns:
            Dict[int, Tuple[int, int]]: a dictionary of the nodes to their label, only returning efficient labels
        """
        efficient_labels = {}
        
        for node, label in self.labels.items():
            other_labels = [ item for item in self.labels.values() if item != label ]
            if not NodeLabel._is_label_dominated_in_list(label[0], label[1], other_labels):
                efficient_labels[node] = label

        return efficient_labels
    
    @staticmethod
    def _is_label_dominated_in_list(weight: int, cost: int, labels: List[Tuple[int, int]]) -> bool:
        """
        Checks if a label is dominated based on the weight and cost. A label is dominated if
        its weight and cost are both less than the weight and cost of another node in the set
        of labels for this node.

        Args:
            weight (int): the weight of the label
            cost (int): the cost of the label
            labels (Sequece): a list of labels

        Returns:
            bool: true if the label is dominated by at least one label in the list of labels
        """
        isDominated = False

        for label in labels:
            if (weight > label[0] and cost > label[1]) or label == (weight, cost):
                isDominated = True
                break

        return isDominated
    
