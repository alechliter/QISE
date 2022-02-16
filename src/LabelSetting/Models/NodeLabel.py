
from typing import Dict, List, Set, Tuple

from src.GraphModeling.models.Graph import Graph
from src.GraphModeling.models.WCGraph import WCGraph


class NodeLabel:
    """
    The Node Label class defines a label-storing object for a node in a weight-constrained graph.
        
    members:
        + node_index (int): the index identifier of the node
        + labels (Dict[int, Tuple(int, int)]): a dictionary of node indicies to labels, of the form:
            L_i = { j : (W_jk + w_ji, C_jk + c_ji) }
        + incoming_nodes (List[int]): a list of indicies of nodes with outgoing edges to this node.
        + outgoing_nodes (List[int]): a list of indicices of nodes with incoming edges from this node.
        + treated_nodes (List[int]): a list of treated nodes for the label (only treats outgoing labels)
        + paths (Dict[int, list[list[int]]]): a dictionary of paths from the source node, through the incoming node, to this node
    """

    def __init__(self, index: int, incoming_nodes: List[int] = [], outgoing_nodes: List[int] = []) -> None:
        """
        Creates a new instance of a NodeLabel object.

        Args:
            index (int): the index identifier of the node
            incoming_nodes (List[int], optional): the list of nodes with outgoing edges going to the node. Defaults to [].
        """
        self.node_index = index
        self.incoming_nodes = incoming_nodes
        self.outgoing_nodes = outgoing_nodes
        self.treated_nodes: List[int] = []
        self.labels: Dict[int, Tuple[int, int]] = { node: () for node in incoming_nodes }
        self.paths: Dict[int, list[list[int]]] = { node: [] for node in incoming_nodes }

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
    
    def get_lowest_weight_label(self) -> Tuple[int,  Tuple[int, int]] | None:
        """
        Finds the label with the lowest weight for this node

        Returns:
            Tuple[int,  Tuple[int, int]] | None: the node and corresponding label with the lowest weight, None if there are no labels
        """
        minimal_label: Tuple[int, int] | None = None
        minimal_node: int = None

        for node, label in self.labels.items():
            if minimal_label is not None and len(label) != 0:
                if label[0] < minimal_label[0] or (label[0] == minimal_label[0] and label[1] < minimal_label[1]):
                    minimal_label = label
                    minimal_node = node
            elif len(label) != 0:
                minimal_label = label
                minimal_node = node

        return (minimal_node, minimal_label)

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

        return NodeLabel._is_label_dominated_in_list(weight, cost, self.labels.values())

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
            if len(label) != 0 and not NodeLabel._is_label_dominated_in_list(label[0], label[1], other_labels):
                efficient_labels[node] = label

        return efficient_labels
    
    def get_untreated_nodes(self) -> Set[int]:
        """
        Returns a set of the remaining indicies not yet treated for a node: I_i - T_i

        Args:
            node (int): the node identifier

        Returns:
            Set[int]: returns a set of node indicies that have not yet been treated for that node
        """
        set_of_indicies = set(self.incoming_nodes)
        set_of_treated = set(self.treated_nodes)
        return set_of_indicies.difference(set_of_treated)
    
    def num_untreated_nodes(self) -> int:
        """
        Returns the number of untreated nodes left for the node

        Returns:
            int: number of untreated nodes
        """
        return len(self.get_untreated_nodes())

    def get_i_paths(self, source: int, incoming_node: int, graph: Graph) -> List[List[int]]:
        """
        Returns a list of all paths from the source node that pass through the given incoming
        node to this node.

        Args:
            source (int): source node in the path
            incoming_node (int): incoming node that the path passes through right before this node
            graph (Graph): graph containing this node

        Returns:
            List[List[int]]: a list of paths
        """
        paths: List[List[int]] = []

        if source != self.node_index:
            if source == incoming_node:
                paths = graph.get_simple_paths(source, self.node_index)
            else:
                paths = graph.get_simple_paths(source, incoming_node)
                if len(paths) != 0:
                    for path in paths:
                        path.append(self.node_index)
        return paths
    
    def get_i_weight_cost(self, source: int, incoming_node: int, graph: WCGraph) -> Tuple[int, int]:
        paths = self.get_i_paths(source, incoming_node, graph)
        if len(paths) > 0:
            weight_cost: tuple[int, int] = graph.calc_path_weight_cost(paths[0])
            for path in paths:
                current_w_c = graph.calc_path_weight_cost(path)
                if current_w_c[0] <= weight_cost[0]:
                    weight_cost = current_w_c
        else:
            weight_cost = None
        return weight_cost
    
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
            if len(label) != 0 and (weight > label[0] and cost > label[1]) or label == (weight, cost):
                isDominated = True
                break

        return isDominated
    
