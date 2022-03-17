from ctypes import sizeof
import numpy
from numpy import random as r

from collections.abc import Sequence

from ...GraphModeling.models.Graph import Graph
from ...GraphModeling.models.WCGraph import WCGraph
from ...LabelSetting.models.LabelAlgorithmRec import LabelAlgorithmRec

import networkx

def main():
    graph_dict = {
        #edge    constraint
        #s  t    w  c
        (0, 1): (1, 1),
        (1, 2): (2, 5),
        (0, 3): (1, 1),
        (1, 3): (2, 2),
        (1, 4): (2, 8),
        (2, 4): (1, 2),
        (3, 4): (6, 2),
    }
    graph = WCGraph(graph_dict)
    graph = WCGraph.load_json_graph("graph_save_test_01")
    
    #Function takes in the graph and a list of efficient paths
    labels = LabelAlgorithmRec()
    labels.run_algorithm(graph, 0, 10)
    x = labels.node_labels[4].paths.values()
    print("Efficient Paths:", x)
    print(list(x))
    p_edges = set({})
    LRG_dict = {} #Lagrangian relaxation graph dictionary
    alpha = 1
    p_sums = []
    for p_nodes in list(x):
        p_sum = 0
        for i in range(0,len(p_nodes)-1):
            edge = (p_nodes[i],p_nodes[i+1])
            new_cost = graph_dict[edge][0] + alpha*graph_dict[edge][1]
            p_sum += new_cost
            LRG_dict[edge] = new_cost
        p_sums.append(p_sum)
    print(p_edges)
    #newcost = cost + alpha*weight

    print(LRG_dict)
    print(p_sums)
    #Function spits out most efficient path
    p_sums.remove(0)
    index = p_sums.index(min(p_sums))
    print("Most efficient path: ", list(x)[index])
    # graph.print_graph(picture_name = f"resources/ArbitraryGraphTestResults/TEST", show_minimal_output = False)

if __name__ == "__main__":
    main()