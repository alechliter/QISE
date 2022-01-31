import random as r
import matplotlib.pyplot as plt
import networkx as nx
from networkx.generators.random_graphs import (fast_gnp_random_graph,
                                               random_kernel_graph)

# DiGraph Testing (Directed Graph)

# ## 1. Trivial Graph
# G1 = nx.DiGraph()

# G1.add_node(1)
# G1.add_node(2)

# G1.add_edge(1,2)

# print("Nodes on Graph:")
# print(G1.nodes())
# print("Edges of Graph:")
# print(G1.edges())

# nx.draw(G1)
# plt.savefig("directed_graph_trival.png") #save as png
# plt.show() #display

# ## 2. Graph from list
# G2 = nx.DiGraph()
# nodes2 = {1,2,3,4,5,6}
# edges2 = {(1,2),(2,3),(5,6),(4,5),(4,6),(3,4),(3,6)}

# G2.add_nodes_from(nodes2)
# G2.add_edges_from(edges2)
# print("Nodes on Graph:")
# print(G2.nodes())
# print("Edges of Graph:")
# print(G2.edges())

# nx.draw(G2)
# plt.savefig("directed_graph_fromlist.png") #save as png
# plt.show() #display

## 3. Arbitrary Directed Graph w/ start and end

### Additional restriction of start and end node
#### No self-loops
#### No ingoing edges from start node
#### No outgoing edges from end node
#### Not necesarilly all paths lead to end node

numNodes = 6   # Choose number of nodes
numEdges = 7   # Choose number of edges
startNode = 0  # Choose start node
endNode = 5    # Choose end node

G3 = nx.DiGraph()
# Add all nodes
for i in range(0,numNodes):
    G3.add_node(i)
# Generate Edges

# Represent edges with dict
## Key: From node
## Items: List of corresponding To nodes
edges = dict()
for i in range(0,numEdges):
    edges[i]=[]


    #Ensure unique non-looping node
for i in range(0,numEdges):
    fromNode = -1
    toNode = -1
    
    # Available "to" nodes
    aToNodes = [*range(numNodes)]
    aToNodes.remove(startNode)

    # Available "from" nodes
    aFromNodes = [*range(numNodes)]
    aFromNodes.remove(endNode)
    
    fromNode = int(r.choice(aFromNodes)) #randomly choose from node from available list
    
    # #No Self Loops
    if(fromNode!=startNode):
        aToNodes.remove(fromNode)
    
    #Remove all current edges from possibility
    
    
    # print(aToNodes)
    toNode = r.choice(aToNodes) #randomly choose node from available list
    print("From Node: " + str(fromNode)+"\t To Node: " + str(toNode))
    edges[fromNode].append(toNode)
    


for i in range(0,numEdges):
    if edges[i]==[]:
        edges.pop(i)
print("Dict Edges:")
print(edges)

listEdges = []
for x in edges.keys():
    for j in range(0,len(edges[x])):
        listEdges.append((x,edges[x][j]))
print("List Edges:")
print(listEdges)

G3.add_edges_from(listEdges)

print("Nodes on Graph:")
print(G3.nodes())
print("Edges of Graph:")
print(G3.edges())

nx.draw(G3)
plt.savefig("directed_graph_random.png") #save as png
plt.show() #display
