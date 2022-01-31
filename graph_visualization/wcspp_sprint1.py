import random as r
import matplotlib.pyplot as plt
import networkx as nx
from networkx.generators.random_graphs import (fast_gnp_random_graph,
                                               random_kernel_graph)
import numpy as np

def main():
    x = np.zeros((5,5))
    w = np.zeros((5,5))
    c = np.zeros((5,5))
    
    x[0][1] = 1
    x[0][3] = 1
    x[1][2] = 1
    x[1][3] = 1
    x[1][4] = 1
    x[2][4] = 1
    x[3][4] = 1
    
    w[0][1] = 1
    w[0][3] = 1
    w[1][2] = 2
    w[1][3] = 2
    w[1][4] = 2
    w[2][4] = 1
    w[3][4] = 6
    
    c[0][1] = 1
    c[0][3] = 1
    c[1][2] = 5
    c[1][3] = 2
    c[1][4] = 8
    c[2][4] = 2
    c[3][4] = 2
    
    print("Graph Direction Matrix:")
    print(x)
    
    G = nx.DiGraph()
    G.add_nodes_from(get_seq(5))
    G.add_edges_from(get_arcs(x))
    
    
    print("\n")
    
    print("All Simple Paths:")
    all_paths = nx.all_simple_paths(G, source=0, target=4)    
    
    wc_paths = []
    for path in all_paths:
        x=[]
        y=[]
        for i in range(0,len(path)-1):
            x.append(w[path[i]][path[i+1]])
            y.append(c[path[i]][path[i+1]])
        print(path,end="\t")
        print("Total Weight, Cost: "+str(sum(x))+", "+str(sum(y)))    
        if sum(x)<=6:
            wc_paths.append((path,sum(y)))

    print("\nWeight Constrained Paths:")
    least_cost_path = wc_paths[0]
    
    for path in wc_paths:
        if path[1]<least_cost_path[1]:
            least_cost_path[0] = path[0]
            least_cost_path[1] = path[1]
        print(path[0],end="\t")
        print("Total Cost: "+str(path[1]))
        
    print("\n Weight Constrained Lowest Cost Path:")
    print(least_cost_path)
    
    print("\n")
    print_graph(G)
    

    """
    get_arcs takes in a matrix x and outputs the (ij) positions of non-zero elements
    as a nested array arcs
    for a digraph matrix this is the "to" and "from" of each arc
    """
def get_arcs(x):
    xnz = np.nonzero(x)
    arcs = []
    for i in range(0,len(xnz[0])):
        arcs.append([xnz[0][i],xnz[1][i]])
    return arcs

"""
    returns a sequential list of numbers 0 to n-1
    """
def get_seq(n):
    return [*range(n)]
    
def get_color_map(n,s=0,t=-1):
    t = n-1 if t==-1 else t-1
    color_map = []
    for i in range(0,n):
        if i==s:
            color_map.append("green")
        elif i==t:
            color_map.append("red")
        else:
            color_map.append("blue")
    return color_map
        

def print_graph(G, picture_name=""):
    print("Nodes on Graph:")
    print(G.nodes())
    print("Edges of Graph:")
    print(G.edges())

    elbs = {
        (0,1): "1,1",
        (0,3): "1,1",
        (1,2): "2,5",
        (1,3): "2,2",
        (1,4): "2,8",
        (2,4): "1,2",
        (3,4): "6,2",
    }
    nx.draw_networkx(G,with_labels=True, pos=nx.circular_layout(G),node_color=get_color_map(len(G)))
    edge_labels=nx.draw_networkx_edge_labels(G, edge_labels=elbs, pos=nx.circular_layout(G))
    
    if picture_name != "":
        plt.savefig(picture_name) #save as png
    plt.show() #display
    
    
if __name__ == "__main__":
    main()