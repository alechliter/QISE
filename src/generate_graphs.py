import networkx as nx
import logging
import matplotlib.pyplot as plt
from numpy import floor
from numpy import random as r
from networkx.readwrite import json_graph
import json

def main():
    print("\nGENERATE WEIGHT COST GRAPHS\n")
    MEAN_WEIGHT = 20
    MEAN_COST = 50
    WEIGHT_STD_DEVIATION = 5
    COST_STD_DEVIATION = 10
    MIN_EDGE_DISTANCE = 5
    
    graph_sizes = [10, 50, 100, 200, 400, 800, 1600, 3200, 6400, 12_800]
    
    for n in graph_sizes:
        random_wc_graph = create_random_wc_graph(n = n, mean_weight = MEAN_WEIGHT, 
                                                 mean_cost = MEAN_COST, 
                                                 std_weight = WEIGHT_STD_DEVIATION, 
                                                 std_cost = COST_STD_DEVIATION, 
                                                 min_edge_distance = MIN_EDGE_DISTANCE)
    
        node_link_data = json_graph.node_link_data(random_wc_graph)
        json_object = json.dumps(node_link_data)
        with open(f"./graphs/wc_graph_{n}.json", "w") as fileout:
            fileout.write(json_object)


def create_random_wc_graph(n: int, mean_weight: int, mean_cost: int, 
                           std_weight: int=1, std_cost: int=1, 
                           min_edge_distance: int=5) -> nx.DiGraph:
    """Generates arbitrary WC graph with n nodes with normally distributed weights and costs."""
    
    wc_graph = nx.DiGraph()
    
    for node_index in range(0, n-1):
        max_edge_distance = min(n-node_index-1, min_edge_distance)
        num_outgoing_edges = r.randint(1, max_edge_distance + 1) if max_edge_distance > 1 else 1
        logging.info(f"{node_index=}\t{max_edge_distance=}\t{num_outgoing_edges=}")
    
        outgoing_nodes = r.choice([*range(node_index+1, min(n-1, node_index + min_edge_distance) + 1)], 
                           num_outgoing_edges, replace = False) if node_index != n-1 else [n]
        
        for outgoing_node_index in outgoing_nodes:
            random_weight_cost = get_random_weight_cost(mean_weight, mean_cost, 
                                                        weight_standard_deviation = std_weight, 
                                                        cost_standard_deviation = std_cost)
            wc_graph.add_edge(int(node_index), int(outgoing_node_index), 
                              weight_cost = random_weight_cost)

        has_incoming_nodes = False
        for k in range(0, node_index):
            if(wc_graph.has_edge(k, node_index)):
                has_incoming_nodes = True
                break
        if not has_incoming_nodes and node_index != 0:
            new_incoming_node = r.randint(max(0, node_index - min_edge_distance), node_index-1) if node_index>1 else 0
            random_weight_cost = get_random_weight_cost(mean_weight, mean_cost, 
                                                        weight_standard_deviation = std_weight, 
                                                        cost_standard_deviation = std_cost)
            wc_graph.add_edge(int(new_incoming_node), int(node_index), 
                              weight_cost = random_weight_cost)
            
    return wc_graph

def get_random_weight_cost(mean_weight: int, mean_cost: int, 
                           weight_standard_deviation:int=1, 
                           cost_standard_deviation:int=1) -> tuple[int, int]:
        """Generates random weight cost tuple from a normal distribution."""
    
        random_weight = int(max(floor(r.normal(mean_weight, weight_standard_deviation)),1))
        random_cost = int(max(floor(r.normal(mean_cost, cost_standard_deviation)), 1))
        return (random_weight, random_cost)

if __name__ == "__main__":
    main()