from ctypes import sizeof
import numpy
from numpy import random as r

from collections.abc import Sequence

from ...GraphModeling.models.Graph import Graph
from ...GraphModeling.models.WCGraph import WCGraph
from ...LabelSetting.models.LabelAlgorithmRec import LabelAlgorithmRec

import networkx

def main():
    graph = WCGraph.load_json_graph("LRTestingGraph")
    max_weight = 400*25
    x = run_label_setting(graph, max_weight)
    
    # graph.print_graph(picture_name = f"resources/ArbitraryGraphTestResults/LRTEST", show_minimal_output = True)
    
    graphs = []
    # for alph in range(1,2):
    [graph_dict, meff_path] = run_dirty_lagrange(graph, 1, x)
    # print(graph_dict)
    LRedges = list(graph_dict.keys())
    
    print("Edges: ", LRedges)
    
    graphLR = Graph(LRedges)
    meff_edges = get_list_of_edges(meff_path)
    graphLR.print_graph(picture_name = f"resources/ArbitraryGraphTestResults/LRTESTsubgraph", show_minimal_output = False, highlight_edges=meff_edges)
            
    

def run_label_setting(graph, max_w):
    #Function takes in the graph and a list of efficient paths
    labels = LabelAlgorithmRec()
    labels.run_algorithm(graph, 0, max_weight=max_w)
    x = labels.node_labels[999].paths.values()
    print("Efficient Paths:", list(x))
    return x

#Returns a list of edges from a list of nodes
def get_list_of_edges(nodes):
    edges = []
    for i in range (0,len(nodes)-1):
        edges.append((nodes[i],nodes[i+1]))
    return edges

#Runs dirty method of the Lagrangian Relaxation algorithm
def run_dirty_lagrange(graph, alpha, paths):
    
    graph_dict = graph.wc_edges
    LRG_dict = {} #Lagrangian relaxation graph dictionary
    p_sums = []
    for p_nodes in list(paths):
        p_sum = 0
        for i in range(0,len(p_nodes)-1):
            edge = (p_nodes[i],p_nodes[i+1])
            #newcost = cost + alpha*weight
            new_cost = graph_dict[edge][0] + alpha*graph_dict[edge][1]
            p_sum += new_cost
            LRG_dict[edge] = new_cost
        p_sums.append(p_sum)
    
    #Lagrangian graph
    print("\nGraph Subset: ", LRG_dict)
    #Path Sums
    print("Path Sums: ", p_sums)
    
    #Remove all zeros from p_sums
    while 0 in p_sums:
        p_sums.remove(0)
        
    #Function spits out most efficient path
    index = p_sums.index(min(p_sums))
    print("Most efficient path: ", list(paths)[index])
    return [LRG_dict, list(paths)[index]]

if __name__ == "__main__":
    main()