import random
from networkx import random_lobster, circular_layout, draw
import matplotlib.pyplot as plt
from networkx.generators.random_graphs import fast_gnp_random_graph, random_kernel_graph


# random graph with 2 >= nodes to graphs

G = random_lobster(40,.5,.2)
# pos = circular_layout(G)
# path_weight(G, path, weight)


print("Nodes on Graph:")
print(G.nodes())
print("Edges of Graph:")
print(G.edges())

draw(G)
plt.savefig("simple_graph.png") #save as png
plt.show() #display
