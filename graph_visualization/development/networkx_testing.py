import matplotlib.pyplot as plt
import networkx as nx
from networkx.generators.random_graphs import (fast_gnp_random_graph,
                                               random_kernel_graph)
import numpy as np

def main():
    G = nx.DiGraph()
    G.add_nodes_from([1,2])
    color_map = ["green","red"]
    nx.draw_networkx(G,pos=nx.circular_layout(G),node_color=color_map)
    plt.show()
    

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
    
def print_graph(G, picture_name=""):
    print("Nodes on Graph:")
    print(G.nodes())
    print("Edges of Graph:")
    print(G.edges())

    nx.draw(G)
    if picture_name != "":
        plt.savefig(picture_name) #save as png
    plt.show() #display
    
    
if __name__ == "__main__":
    main()