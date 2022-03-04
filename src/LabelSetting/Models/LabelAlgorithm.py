from typing import Dict, List, Set, Tuple

from ...GraphModeling.models.WCGraph import WCGraph
from ...GraphModeling.models.Graph import Graph
from .NodeLabel import NodeLabel

class LabelAlgorithm:
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
    
    def run_algorithm_v1(self, graph: WCGraph, source_node: int, max_weight: int):
        """
        Runs the Label Setting Algorithm on the given weight-constrained graph with the given source node.

        v1 - finds the path for from the source to every single node. Accurate but very inefficient. Use this
             only to check if other label setting algorithms are working properly.

        Args:
            graph (WCGraph): the weight-constrained graph
            source_node (int): the index that defines the source node
            max_weight (itn): the maximum weight constraint
        """
        self.graph = graph
        self.source_node = source_node
        self.max_weight = max_weight 

        # Step 0: Initialize the labels
        self._initialize_label_setup()

        # Step 1a: Select a label to be treated
        while len(self._get_remaining_label_indicies()) != 0:
            current_node = self._get_next_node()
            if current_node:
                i = current_node.node_index
                # Step 1b: select an untreated index of the node such that the total weight is minimal
                #   meaning: given node i, select node index k from the list of untreated incoming nodes to i such 
                #            that the weight of the edge (k, i) is the smallest among incoming edges to i
                if current_node.node_index != self.source_node:
                    untreated_in_nodes = current_node.get_untreated_nodes()
                    k_in = untreated_in_nodes.pop()
                    k_i_W_C = current_node.get_i_weight_cost(self.source_node, k_in, self.graph)
                    for j_in in untreated_in_nodes:
                        j_i_W_C = current_node.get_i_weight_cost(self.source_node, j_in, self.graph)
                        if j_i_W_C[0] < k_i_W_C[0]:
                            k_in = j_in
                            k_i_W_C = j_i_W_C
                else:
                    k_i_W_C = (0, 0)
                    k_in = self.source_node
                # Step 2: Treat the label
                W_k_i = k_i_W_C[0]  # the weight of the path [s, ..., k, i]
                C_k_i = k_i_W_C[1]  # the cost of the path [s, ..., k, i]
                for j_out in current_node.outgoing_nodes:
                    w_i_j = self.graph.wc_edges[i, j_out][0]       # the weight of edge (i, j)
                    total_weight = W_k_i + w_i_j
                    if total_weight <= self.max_weight:
                        c_i_j = self.graph.wc_edges[i, j_out][1]   # cost of the edge (i, j)
                        total_cost = C_k_i + c_i_j
                        if not self.node_labels[j_out].is_label_dominated(total_weight, total_cost):
                            # add the label to the next node: j
                            self.node_labels[j_out].add_label(total_weight, total_cost, current_node.node_index)
                            # add the corresponding path from the source node to node j
                            path_s_i = self.node_labels[k_in].get_lowest_weight_path()  # path from source node s to current node i
                            if current_node.node_index != self.source_node:
                                path_s_i += [current_node.node_index]
                            self.node_labels[j_out].add_path(path_s_i, current_node.node_index)

                current_node.treated_nodes.append(k_in)
            else:
                print("Error: untreated nodes remain yet no next node found")
                break

    def run_algorithm_v2(self, graph: WCGraph, source_node: int, max_weight: int):
        """
        Runs the Label Setting Algorithm on the given weight-constrained graph with the given source node.

        v2 - start from the source node and work outward until every node has been treated

        Args:
            graph (WCGraph): the weight-constrained graph
            source_node (int): the index that defines the source node
            max_weight (itn): the maximum weight constraint
        """
        self.graph = graph
        self.source_node = source_node
        self.max_weight = max_weight 

        # Step 0: Initialize the labels
        self._initialize_label_setup()

        # Step 1a: Select a label to be treated
        while len(self._get_remaining_label_indicies()) != 0:

            # Step 1b: select an untreated index of the node such that the total weight is minimal
            #   meaning: given node i, select node index k from the list of untreated incoming nodes to i such 
            #            that the weight of the edge (k, i) is the smallest among incoming edges to i
            current_node: NodeLabel = self._rec_next_node(self.source_node)
            print(f"Current Node: {current_node.node_index}")
            if current_node is not None:
                i = current_node.node_index
                k_in: int = None
                k_label: Tuple[int, int] = None
                W_k_i:int
                C_k_i:int
                if current_node.node_index != self.source_node:
                    # find the incoming node with a label with the lowest weight
                    for j_in in current_node.get_untreated_nodes():
                        j_label = self.node_labels[j_in].get_lowest_weight_label()[1]
                        if k_label is not None and j_label is not None:
                            if j_label[0] < k_label[0] or (j_label[0] == k_label[0] and j_label[1] < k_label[1]):
                                k_in = j_in
                                k_label = j_label
                        elif k_label is None:
                            k_in = j_in
                            k_label = j_label
                    if k_label is not None:
                        W_k_i = k_label[0] + self.graph.wc_edges[k_in, i][0]    # the weight of the path [s, ..., k, i]
                        C_k_i = k_label[1] + self.graph.wc_edges[k_in, i][1]    # the cost of the path [s, ..., k, i]
                    else:
                        # Special case: only incoming nodes that don't have any labels are untreated, skip for now.
                        current_node.treated_nodes.append(k_in)
                        current_node.needs_visit = False
                        continue
                else:
                    # current node is the source node, so no incoming nodes exists (that we care about)
                    k_in = current_node.node_index
                    k_label = current_node.labels[0]
                    W_k_i = k_label[0]
                    C_k_i = k_label[1]

                # Step 2: Treat the label
                for j_out in current_node.outgoing_nodes:
                    w_i_j = self.graph.wc_edges[i, j_out][0]       # the weight of edge (i, j)
                    total_weight = W_k_i + w_i_j
                    if total_weight <= self.max_weight:
                        c_i_j = self.graph.wc_edges[i, j_out][1]   # cost of the edge (i, j)
                        total_cost = C_k_i + c_i_j
                        if not self.node_labels[j_out].is_label_dominated(total_weight, total_cost):
                            # add the label to the next node (j) and remove that node from treated lists
                            self.node_labels[j_out].add_label(total_weight, total_cost, current_node.node_index)
                            # add the corresponding path from the source node to node j
                            path_s_i = self.node_labels[k_in].get_lowest_weight_path()  # path from source node s to current node i
                            if current_node.node_index != self.source_node:
                                path_s_i += [current_node.node_index]
                            self.node_labels[j_out].add_path(path_s_i, current_node.node_index)
                            # update outgoing nodes from node j, signaling that they now need to be re-treated for node j
                            for node in self.node_labels[j_out].outgoing_nodes:
                                if j_out in self.node_labels[node].treated_nodes:
                                    self.node_labels[node].treated_nodes.remove(j_out)


                current_node.treated_nodes.append(k_in)
                current_node.needs_visit = False
            else:
                print("Error: untreated nodes remain yet no next node found")
                break

    def gen_all_possible_labels(self, graph: WCGraph, source_node: int, max_weight: int):
        """
        Runs a modified version of the Label Setting Algorithm on the given weight-constrained graph 
        with the given source node. This function generates all possible labels, ignoring the maximum 
        weight constraint and including all labels, even when dominated. This algorithm does not give
        the path with the lowest weight, but it does generate all labels for every path, with a chance
        of overwritting labels.

        v2 - start from the source node and work outward until every node has been treated

        Args:
            graph (WCGraph): the weight-constrained graph
            source_node (int): the index that defines the source node
            max_weight (itn): the maximum weight constraint
        """
        self.graph = graph
        self.source_node = source_node
        self.max_weight = max_weight 

        # Step 0: Initialize the labels
        self._initialize_label_setup()

        # Step 1a: Select a label to be treated
        while len(self._get_remaining_label_indicies()) != 0:

            # Step 1b: select an untreated index of the node such that the total weight is minimal
            #   meaning: given node i, select node index k from the list of untreated incoming nodes to i such 
            #            that the weight of the edge (k, i) is the smallest among incoming edges to i
            current_node: NodeLabel = self._rec_next_node(self.source_node)
            print(f"Current Node: {current_node.node_index}")
            if current_node is not None:
                i = current_node.node_index
                k_in: int = None
                k_label: Tuple[int, int] = None
                W_k_i:int
                C_k_i:int
                if current_node.node_index != self.source_node:
                    # find the incoming node with a label with the lowest weight
                    for j_in in current_node.get_untreated_nodes():
                        j_label = self.node_labels[j_in].get_lowest_weight_label()[1]
                        if k_label is not None and j_label is not None:
                            if j_label[0] < k_label[0] or (j_label[0] == k_label[0] and j_label[1] < k_label[1]):
                                k_in = j_in
                                k_label = j_label
                        elif k_label is None:
                            k_in = j_in
                            k_label = j_label
                    if k_label is not None:
                        W_k_i = k_label[0] + self.graph.wc_edges[k_in, i][0]    # the weight of the path [s, ..., k, i]
                        C_k_i = k_label[1] + self.graph.wc_edges[k_in, i][1]    # the cost of the path [s, ..., k, i]
                    else:
                        # Special case: only incoming nodes that don't have any labels are untreated, skip for now.
                        current_node.treated_nodes.append(k_in)
                        current_node.needs_visit = False
                        continue
                else:
                    # current node is the source node, so no incoming nodes exists (that we care about)
                    k_in = current_node.node_index
                    k_label = current_node.labels[0]
                    W_k_i = k_label[0]
                    C_k_i = k_label[1]

                # Step 2: Treat the label
                for j_out in current_node.outgoing_nodes:
                    w_i_j = self.graph.wc_edges[i, j_out][0]       # the weight of edge (i, j)
                    total_weight = W_k_i + w_i_j
                    c_i_j = self.graph.wc_edges[i, j_out][1]        # cost of the edge (i, j)
                    total_cost = C_k_i + c_i_j
                    # add the label to the next node (j) and remove that node from treated lists
                    self.node_labels[j_out].add_label(total_weight, total_cost, current_node.node_index)
                    for node in self.node_labels[j_out].outgoing_nodes:
                        if j_out in self.node_labels[node].treated_nodes:
                            self.node_labels[node].treated_nodes.remove(j_out)
                    # add the corresponding path from the source node to node j
                    path_s_i = self.node_labels[k_in].get_lowest_weight_path()  # path from source node s to current node i
                    if current_node.node_index != self.source_node:
                        path_s_i += [current_node.node_index]
                    self.node_labels[j_out].add_path(path_s_i, current_node.node_index)                    

                current_node.treated_nodes.append(k_in)
                current_node.needs_visit = False
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
    
    def _get_next_node(self) -> NodeLabel | None:
        """
        Gets the next node with untreated incoming node-labels

        Returns:
            [NodeLabel | None]: returns either the next node if one exists or None.
        """
        next_node: NodeLabel | None = None

        for node in self.node_labels.values():
            if len(node.get_untreated_nodes()) != 0:
                next_node = node
                break
        print (next_node.node_index)

        return next_node
    
    def _rec_next_node(self, from_node: int) -> NodeLabel | None:
        """
        Recursively finds the next node with untreated node-labels in the graph, treating the graph
        as a tree with [from_node] as the root.

        Args:
            from_node (int): node index to check to begin search at as the root

        Returns:
            NodeLabel | None: the next node to treat
        """
        # case 1: all nodes have been treated from this tree 
        # (found_node is a leaf - a node with no outgoing nodes)
        next_node: NodeLabel | None = None

        if self.node_labels[from_node].num_untreated_nodes() > 0:
            # case 2: from_node has untreated nodes
            next_node = self.node_labels[from_node]
        else:
            # case 3: from_node has all treated nodes
            child_nodes = self.node_labels[from_node].outgoing_nodes
            if len(child_nodes) > 0:
                # check each child node for any untreated nodes. Stop when one is found
                untreated_children = []
                for child in child_nodes:
                    child_node = self.node_labels[child]
                    if child_node.num_untreated_nodes() > 0:
                        untreated_children.append(child_node)
                if len(untreated_children) > 0:
                    next_node = untreated_children.pop()
                else:
                    # case 4: all child nodes have treated nodes: call _rec_next_node on each until one is found
                    for child in child_nodes:
                        next_node = self._rec_next_node(child)
                        if next_node is not None:
                            break
        return next_node