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
    num_nodes = 1000
    mean_weight = 25
    max_weight = int(num_nodes*mean_weight*(0.8))
    eff_paths = list(run_label_setting(graph, max_weight, num_nodes))
    # eff_paths = [[0, 34, 59, 99], [0, 30, 60, 99], [0, 30, 61, 99], [], [0, 34, 63, 99], [], [], [0, 30, 67, 99], [0, 30, 68, 99], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    # print(eff_paths)
    graph.print_graph(picture_name = f"resources/ArbitraryGraphTestResults/LRTEST", show_minimal_output = True)
    
    for i in range(len(eff_paths)-1,0-1,-1):
        print(i)
        if len(eff_paths[i]) < 1:
            eff_paths.remove(eff_paths[i])
    # print("eff_paths: ", eff_paths)
    
    for alph in range(1,5):
        print("Alpha = "+str(alph)+":")
        [graph_dict, meff_path] = run_dirty_lagrange(graph, alph, eff_paths)
        # print(graph_dict)
        LRedges = list(graph_dict.keys())
        
        print("\nMax Weight: ", max_weight)
        print("Edges: ", LRedges)
        print("Most Efficient Path: ", meff_path)
        
        graphLR = Graph(LRedges)
        meff_edges = get_list_of_edges(meff_path)
        graphLR.print_graph(picture_name = f"resources/ArbitraryGraphTestResults/LRTESTsubgraph_a"+str(alph), show_minimal_output = False, highlight_edges=meff_edges)
        print("-----------------------------------------------------------\n")
            
    

def run_label_setting(graph, max_w, num_nodes):
    #Function takes in the graph and a list of efficient paths
    labels = LabelAlgorithmRec()
    labels.run_algorithm(graph, 0, max_weight=max_w)
    x = labels.node_labels[num_nodes-1].paths.values()
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
    # print("Path Sums: ", p_sums)
    
    #Function spits out most efficient path
    index = p_sums.index(min(p_sums))
    # print("Most efficient path: ", list(paths)[index])
    return [LRG_dict, list(paths)[index]]

if __name__ == "__main__":
    main()