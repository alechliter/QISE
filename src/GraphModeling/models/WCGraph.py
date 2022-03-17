from asyncio import constants
from copyreg import constructor
import json
import numpy
from os.path import exists
from numpy import random as r

from typing import Dict, List, Tuple

from .Graph import Graph

class WCGraph(Graph):
    """Weight-Constrained Graph extends the normal graph, adding functionality specific to 
    the weight-constrained problem.

    members: 
        + weight_matrix (numpy.ndarray): matrix of the weights for each edge
        + cost_matrix (numpy.ndarray): matrix of the costs for each edge
        + wc_edges ( Dict[Tuple[int, int], Tuple[int, int]]): dictionary of edges to (weight, cost)

    note: this might be useless/overkill for our purposes, we could just add everything to the graph class.
    """

    def __init__(self, edges: Dict[Tuple[int, int], Tuple[int, int]]) -> None:
        """Creates a new instance of a Weight-Constrained Graph using a dictionary of edges to weights and costs.

        Args:
            edges (Mapping): a dictionary of edges to their weights and costs {(from, to): (weight, cost)}
        """
        self.wc_edges = edges
        self.weight_matrix: numpy.ndarray
        self.cost_matrix: numpy.ndarray

        # Initialize the base class Graph
        super(WCGraph, self).__init__(edges.keys())

        # Generate Weight and Cost Matricies
        self._generate_weight_cost_matricies()

        pass
    
    def get_arbitrary_graph(n: int, mean_weight: int, mean_cost: int, std_weight:int=1, std_cost:int=1, peak: int=5) -> Graph:
        """Generates arbitrary WC graph with n nodes with normally distributed weights and costs

        Args:
            n (int): number of nodes
            mean_weight (int): mean weight
            mean_cost (int): mean cost
            std_weight (int): standard deviation of weight
            std_cost (int): standard deviation of cost
            peak (int): max number of nodes ahead a node can have an edge to

        Returns:
            Graph: arbitary WC graph with (w,c) normally distributed
        """
        graphDict = {}
        #Loop i range(0,n)
        for i in range(0,n-1):
            #Random Noe range(i,n) # of outgoing edges
            n_forward = min(n-i-1, peak)
            N_oe = r.randint(1,n_forward+1) if n_forward > 1 else 1 #num outgoing edges
            # print("i:", i, "\tn_forward:", n_forward, "\tN_oe:", N_oe)
            #Choose Noe unique nodes range(1,n) delta_o[]
            #TODO: Peaking variable happens here
            delta_o = r.choice([*range(i+1,min(n-1,i+peak)+1)], N_oe, replace=False) if i!=n-1 else [n]
            #For each j in delta_o[], add edge (i,j)
            for j in delta_o:
                graphDict[i,j] = WCGraph.get_random_weight_cost(mean_weight, mean_cost, std_weight=std_weight, std_cost=std_cost)
            #If no incoming nodes
            oneInNode = False
            for k in range(0,i):
                if((k,i) in graphDict):
                    oneInNode = True
                    break
            if not oneInNode and i != 0:
                #Choose node incoming n_in range(0,i-1)
                n_in = r.randint(max(0,i-peak),i-1) if i>1 else 0
                #Add edge (n_in,i)
                graphDict[n_in,i] = WCGraph.get_random_weight_cost(mean_weight, mean_cost, std_weight=std_weight, std_cost=std_cost)
            
        return WCGraph(graphDict)
    
    def find_wc_paths(self, weight: int, source_node: int = 0, destination_node: int | None = None) -> List[List[int]]:
        """Creates a list of each path in the graph that follows the weight constraint.

        Args:
            weight (int): the weight constraint for the paths

        Returns:
            List[List[int]]: a list of paths that follow the weight constraint
        """
        wc_paths = []

        for path in self.get_simple_paths(source_node, destination_node):
            path_weight_cost = self.calc_path_weight_cost(path)
            if path_weight_cost[0] <= weight:
                wc_paths.append(path)

        return wc_paths
    
    def find_lowest_cost_path(self, paths: List[List[int]]) -> List[int]:
        """
        Finds the path with the lowest cost given a list of paths.

        Args:
            paths (List[List[int]]): a list of paths (lists of node pairs)

        Returns:
            List[int]: the path with the lowest cost
        """
        lowest_cost_path = []

        if len(paths) > 0:
            lowest_cost_path = paths[0]
            lowest_cost = self.calc_path_weight_cost(paths[0])[1]
            for path in paths:
                path_weight_cost = self.calc_path_weight_cost(path)
                if path_weight_cost[1] < lowest_cost:
                    lowest_cost_path = path
                    lowest_cost = path_weight_cost[1]

        return lowest_cost_path

    def calc_path_weight_cost(self, path: List[int]) -> Tuple[int, int]:
        """calculates the total weight and cost along a given path

        Args:
            path (List[int]): the path of nodes (an array of nodes in order of path traversal)

        Returns:
            Tuple[int, int]: the total [weight, cost] along the path
        """
        total_weight = 0
        total_cost = 0

        for index in range(len(path) - 1):
            edge = (path[index], path[index + 1])
            total_weight += self.wc_edges[edge][0] # weight
            total_cost += self.wc_edges[edge][1] # cost

        return (total_weight, total_cost)

    def print_graph(self, picture_name: str = "", show_minimal_output: bool = False, highlight_edges = []) -> None:
        """
        Prints the graph with (weight, cost) labels for each edge

        Args:
            picture_name (str, optional): The name of the file to save the picture to. Defaults to "".
            suppress_text_output: Supresses print statements and edge labels from being printed on the graph
        """
        edge_labels = {}

        for edge, constraints in self.wc_edges.items():
            edge_labels[edge] = f"{constraints[0]}, {constraints[1]}"

        super(WCGraph, self).print_graph(picture_name, edge_labels, show_minimal_output, highlight_edges)
    
    def save_to_json(self, graph_name: str):
        json_object = self._gen_json_object()
        with open(WCGraph.get_json_file_name(graph_name), "w") as file:
            json.dump(json_object, file)

    def _generate_weight_cost_matricies(self):
        """
        Generates the weight and cost matrices based on the weights and costs associated with each pair
        in the dictionary wc_edges
        """
        # initialize matrix to nxn 0 matrix
        self.weight_matrix = Graph._gen_zero_n_square_matrix(self.edges)
        self.cost_matrix = Graph._gen_zero_n_square_matrix(self.edges)

        for edge, constraints in self.wc_edges.items():
            self.weight_matrix[edge[0] - 1][edge[1] - 1] = constraints[0]
            self.cost_matrix[edge[0] - 1][edge[1] - 1] = constraints[1]
    
    def _gen_json_object(self) -> json:
        """
        Returns a json object representing the edges with their corresponding weights and costs.

        Returns:
            json: a json object representing the wc_edges dictionary
        """
        json_object = {}
        for edge, constraints in self.wc_edges.items():
            json_object[f"{edge[0]} {edge[1]}"] = {}
            json_object[f"{edge[0]} {edge[1]}"]["weight"] = constraints[0]
            json_object[f"{edge[0]} {edge[1]}"]["cost"] = constraints[1]
        return json_object
    
    @staticmethod
    def load_json_graph(graph_name: str) -> None | Graph:
        """
        Loads a WCGraph object from the given file. If the file doesn't exist, it returns None.

        Args:
            graph_name (str): the name of the graph (not the full file location, just the name of the graph used to save it)

        Returns:
            None | Graph: the graph object representing that graph. Returns None if file doesn't exist.
        """
        graph: WCGraph | None = None
        filename = WCGraph.get_json_file_name(graph_name)

        if exists(filename):
            wc_edges = {}
            with open(filename, 'r') as file:
                json_obj = json.load(file)
                for edge in json_obj:
                    # convert the string representation of the nodes to a tuple of integer values
                    nodes = [int(node) for node in edge.split(" ")]
                    new_edge = tuple(nodes)
                    # combine the weights and costs into a tuple
                    new_constraints = (json_obj[edge]["weight"], json_obj[edge]["cost"])
                    # add the edge-constraint pair to the dictionary of edges to constraints
                    wc_edges[new_edge] = new_constraints
            graph = WCGraph(wc_edges)

        return graph

    @staticmethod
    def get_json_file_name(graph_name: str) -> str:
        """
        Given the name of a graph, this function returns the full path location to the
        corresponding file (relative to the base project folder).

        Args:
            graph_name (str): name of the graph used to save the graph

        Returns:
            str: the full file path, relative to the base project folder
        """
        filename = "".join(graph_name.split(" "))
        return f"resources/SavedGraphs/{filename}.json"

    @staticmethod
    #TODO: Maybe turn this into a lambda function inside of the arbitrary graph generatork
    def get_random_weight_cost(mean_weight: int, mean_cost: int, std_weight:int=1, std_cost:int=1) -> tuple[int, int]:
        """Generates a random cost-weight tuple based on input. Currently normal dist, but could test with other modes

        Args:
            mean_weight (int): mean weight in normal distribution
            mean_cost (int): mean cost in normal distribution
            std_weight (int, optional): standard deviation of weight. Defaults to 1.
            std_cost (int, optional): standard deviation of cost. Defaults to 1.

        Returns:
            _type_: random weight-cost tuple integers
        """    
        #choose random cost and weight (normal)
        random_weight = int(max(numpy.floor(r.normal(mean_weight,std_weight)),1))
        random_cost = int(max(numpy.floor(r.normal(mean_cost,std_cost)),1))
        
        return (random_weight,random_cost)