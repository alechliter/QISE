import networkx as nx
import logging
import json
import time

def main():
    print("\nBENCHMARK LAGRANGIAN RELAXATION SHORTEST PATH ALGORITHM\n")
    benchmark()

def tictoc(func):
    def wrapper():
        t1 = time.time()
        func()
        t2 = time.time() - t1
        print(f"Took {t2} seconds")
    return wrapper

def lagrange_relax_graph(wc_graph: nx.DiGraph, alpha: float) -> nx.DiGraph:
    """Applies Lagrangian relaxation on weight cost graph"""
    
    lagrange_relaxed_graph = nx.DiGraph()
    for n, nbrs in wc_graph.adjacency():
        for nbr, edict in nbrs.items():
            weight_cost = edict["weight_cost"]
            lrvalue = weight_cost[0] + alpha*weight_cost[1]
            lagrange_relaxed_graph.add_edge(n, nbr, weight = lrvalue)
            logging.info(f"({n}, {nbr}): {lrvalue}")
            
    return lagrange_relaxed_graph

def lr_shortest_path(wc_graph: nx.DiGraph, alpha: float) -> list:
    lr_graph = lagrange_relax_graph(wc_graph, alpha)
    n = lr_graph.number_of_nodes()
    return nx.shortest_path(lr_graph, 0, n-1)

@tictoc
def benchmark():
    graph_sizes = [10, 50, 100, 200, 400, 800, 1600, 3200, 6400, 12_800]
    ALPHA = 0.5
    for n in graph_sizes:
        f = open(f"./graphs/wc_graph_{str(n)}.json")
        data = json.load(f)
        random_wc_graph = nx.node_link_graph(data)
        lr_shortest_path(random_wc_graph, ALPHA)

if __name__ == "__main__":
    main()