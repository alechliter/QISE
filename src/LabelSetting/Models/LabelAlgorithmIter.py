from src.GraphModeling.models.WCGraph import WCGraph
from src.LabelSetting.Models.LabelAlgorithmBase import LabelAlgorithmBase
from src.LabelSetting.Models.NodeLabel import NodeLabel


class LabelAlgorithmIter(LabelAlgorithmBase):

    def run_algorithm(self, graph: WCGraph, source_node: int, max_weight: int):
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