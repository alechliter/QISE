from lib2to3.pytree import Node
from typing import List, Tuple
from src.GraphModeling.models.WCGraph import WCGraph
from src.LabelSetting.Models.LabelAlgorithmBase import LabelAlgorithmBase
from src.LabelSetting.Models.NodeLabel import NodeLabel


class LabelAlgorithmRec(LabelAlgorithmBase):

    def __init__(self) -> None:
        super().__init__()
        self.min_percent_remain: float = 0.1

    def run_algorithm(self, graph: WCGraph, source_node: int, max_weight: int):
        """
        Runs the Label Setting Algorithm on the given weight-constrained graph with the given source node.

        v2 - start from the source node and work outward until every node has been treated

        Args:
            graph (WCGraph): the weight-constrained graph
            source_node (int): the index that defines the source node
            max_weight (int): the maximum weight constraint
            min_percent_remain (float): the minimum percentage of remaining nodes to switch searching method
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
            current_node: NodeLabel = self._get_next_node(self.source_node, self.min_percent_remain)
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
    
    def _get_next_node(self, from_node: int, min_percent_remain: float = 0.1) -> NodeLabel | None:
        """
        Finds the next node to be treated. Uses the recursive algorithm to walk from the source to each if there
        many nodes remaining. If only a few remain (determined by a given percentage), then go to those nodes
        directly.

        Args:
            from_node (int): node index to check to begin search at as the root
            min_percent_remain (float, optional): the minimum percentage of remaining nodes to switch searching method. Defaults to 0.01.

        Returns:
            NodeLabel | None:  the next node to treat
        """
        next_node: NodeLabel | None = None

        remaining_nodes = []

        for node, node_label in self.node_labels.items():
            if node_label.num_untreated_nodes() > 0:
                remaining_nodes.append(node)
        
        percent_left: float = len(remaining_nodes) / len(self.node_labels.keys())

        if percent_left > min_percent_remain:
            next_node = self._rec_next_node(from_node)
        else:
            print(f"remaining nodes: {remaining_nodes}")
            for node in remaining_nodes:
                next_node = self._find_earliest_remaining_node(node)
                if next_node:
                    break

        return next_node
    
    def _find_earliest_remaining_node(self, node: int) -> NodeLabel:
        """
        Given a node index with untreated labels, it checks if the incoming nodes to the node also have
        untreated labels. If any do, it continues down that path until it finds a node with untreated labels
        without any direct incoming nodes that also need to be treated. 

        Args:
            node (int): a remaining node to start searching from

        Returns:
            _type_: a node label that needs to be treated.
        """
        earliest_remaining_node = self.node_labels[node]

        for incoming_node in self.node_labels[node].incoming_nodes:
            if self.node_labels[incoming_node].num_untreated_nodes() > 0:
                earliest_remaining_node = self._find_earliest_remaining_node(incoming_node)
                break

        return earliest_remaining_node


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
