from typing import Tuple
from src.GraphModeling.models.WCGraph import WCGraph
from src.LabelSetting.models.LabelAlgorithmBase import LabelAlgorithmBase
from src.LabelSetting.models.NodeLabel import NodeLabel
from src.LabelSetting.models.SpanningTree import SpanningTree, TreeNode


class LabelAlgorithmSpanTree(LabelAlgorithmBase):

    def run_algorithm(self, graph: WCGraph, source_node: int, max_weight: int):
        """
        Runs the Label Setting Algorithm on the given weight-constrained graph with the given source node.

        v3 - generate a spanning tree and traverse that tree

        WARNING: DO NOT USE THIS VERSION

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
        self.spanning_tree = SpanningTree(self.source_node, self.node_labels)
        SpanningTree.print_tree(self.spanning_tree.root)

        # Step 1a: Select a label to be treated
        while len(self._get_remaining_label_indicies()) != 0:

            # Step 1b: select an untreated index of the node such that the total weight is minimal
            #   meaning: given node i, select node index k from the list of untreated incoming nodes to i such 
            #            that the weight of the edge (k, i) is the smallest among incoming edges to i
            current_node: NodeLabel = self._rec_next_node_spantree(self.spanning_tree.root)
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
        
    def _rec_next_node_spantree(self, root: TreeNode) -> NodeLabel | None:
        """
        Recursively finds the next node with untreated node-labels in the graph, treating the graph
        as a tree with [from_node] as the root.

        Version 2: Converting the graph into a spanning tree

        Args:
            from_node (int): node index to check to begin search at as the root

        Returns:
            NodeLabel | None: the next node to treat
        """
        
        next_node = None

        if self.node_labels[root.index].num_untreated_nodes() > 0:
            next_node = self.node_labels[root.index]
        else:
            for child in root.children:
                next_node = self._rec_next_node_spantree(child)
                if next_node:
                    break

        return next_node