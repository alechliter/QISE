import numpy
from collections.abc import Sequence
from ..models.WCGraph import WCGraph
import networkx
import matplotlib.pyplot as pyplot

#Create some graph
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

graph = networkx.DiGraph()
graph.add_edges_from(graph_dict)

#Highlight one edge on that Graph
pos = networkx.circular_layout(graph)
networkx.draw_networkx(graph, pos = pos)
networkx.draw_networkx_edges(
    graph,
    pos,
    edgelist=[(1, 2), (2, 4)],
    width=8,
    alpha=0.5,
    edge_color="tab:red",
)
pyplot.show()



#Create WCSPP arbitrary graph
#Find solution to graph
#Highlight shortest path

