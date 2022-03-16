from ctypes import sizeof
import numpy
from numpy import random as r

from collections.abc import Sequence

from ..models.Graph import Graph
from ..models.WCGraph import WCGraph

import networkx

def main():
    graph = WCGraph({
        #edge    constraint
        #s  t    w  c
        (0, 1): (1, 1),
        (1, 2): (2, 5),
        (0, 3): (1, 1),
        (1, 3): (2, 2),
        (1, 4): (2, 8),
        (2, 4): (1, 2),
        (3, 4): (6, 2),
    })
    graph = WCGraph.load_json_graph("graph_save_test_01")
    graph.print_graph(picture_name = f"resources/ArbitraryGraphTestResults/TEST", show_minimal_output = True)
    paths = [[1,2,3,5],[1,3]]
    #Function takes in the graph and a list of efficient paths
    #newcost = cost + lambda*weight
    #Function spits out most efficient path

if __name__ == "__main__":
    main()