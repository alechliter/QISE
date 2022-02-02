import matplotlib.pyplot as pyplot
import networkx
import numpy

from collections.abc import Sequence

class Graph:
    """ 
    The Graph class allows for the generation of directed graphs containing weights and costs.

    members:
        + edges (Sequence): a list of (from, to) node tuples
        + direction_matrix (numpy.ndarray): matrix of the directed edges between nodes
        + networkx_graph (networkx.DiGraph): networkx object representation of graph
    """
    
    def __init__(self, edges: Sequence) -> None:
        """
        Creates a new instance of the Graph class. Initializes the graph's 
        matricies based on the given general matrix.  

        Args:
            edges (Sequence): a list of edges (node from-to tuples)
        """
        self.edges: Sequence = edges
        self.connection_matrix: numpy.ndarray
        self.networkx_graph: networkx.DiGraph

        # Initialize connection matrix using the list of edges
        self._initialize_connection_matrix()

        # Initialize the networkx graph
        self._initialize_networkx_graph()

        
    def print_graph(self, source_node: int = 0, destination_node: int = -1, picture_name: str = "") -> None:
        """
        Prints the graph using the networkx graph representation and pyplot.

        Args:
            source_node (int, optional): The source node of a path. Defaults to 0.
            destination_node (int, optional): The destination node of a path. Defaults to -1.
            picture_name (str, optional): The name to save the graph image as. Defaults to "".
        """
        print("Nodes on Graph:")
        print(self.networkx_graph.nodes())
        print("Edges of Graph:")
        print(self.networkx_graph.edges())

        networkx.draw_networkx(self.networkx_graph, pos = networkx.circular_layout(self.networkx_graph), node_color = self.get_color_map(3))
        
        if picture_name != "":
            pyplot.savefig(picture_name) #save as png
        pyplot.show() #display

    def get_simple_paths(self, source_node: int, destination_node: int) -> Sequence:
        """
        Returns an array of simple paths in the graph

        Args:
            source_node(int): the first node in the path
            destination_node(int): the last node in the path

        Returns:
            Sequence: a list of paths (a path is an array of nodes)
        """
        paths = []

        if self.networkx_graph:
            paths = networkx.all_simple_paths(self.networkx_graph, source_node, destination_node)

        return paths
    
    def get_color_map(self, n: int, s: int = 0, t: int = -1) -> Sequence:
        """
        Returns a colop mapping for each node in the graph

        Args:
            n (int): the number of nodes
            s (int, optional): The starting node. Defaults to 0.
            t (int, optional): The destination node. Defaults to -1.

        Returns:
            Sequence: a color mapping of each node in the graph
        """
        if t == -1:
            t = n - 1
        else:
             t - 1
        color_map = []
        for i in range(0,n):
            if i == s:
                color_map.append("green")
            elif i == t:
                color_map.append("red")
            else:
                color_map.append("blue")    
        return color_map
    
    def _initialize_networkx_graph(self) -> None:
        """
        Initializes the networkx graph, adding the nodes and edges of the graph 
        to the networkx object.
        """
        self.networkx_graph = networkx.DiGraph()
        # Add nodes
        self.networkx_graph.add_nodes_from(Graph.get_nodes(self.edges))
        # Add edges
        self.networkx_graph.add_edges_from(self.edges)

    def _initialize_connection_matrix(self) -> None:
        """
        Initializes the connection matrix representation of the graph using the defined edges
        for the graph.

        About Connection Matrix: 
        + We are representing a graph using an nxn square matrix, where n = number of nodes.
        + Each matrix element represents an edges between two nodes, where 1 at position M[a][b] 
        indicates that an edges exists between the nodes a and b.
        + The column of the martix represents the "from" nodes and the row represents the "to" nodes, 
        so you can represent directed graphs using the matrix.

            3x3 Example: list of edges --> [(1, 2), (1, 3)]
                     1  2  3
                 1 [[0, 1, 1],
                 2  [0, 0, 0], 
                 3  [0, 0, 0]]
        """
        # initialize matrix to nxn 0 matrix
        nodes = Graph.get_nodes(self.edges)
        num_nodes = len(nodes)
        self.connection_matrix = numpy.zeros((num_nodes, num_nodes))

        for edge in self.edges:
            self.connection_matrix[edge[0] - 1][edge[1] - 1] = 1

    # Static/Class Function
    def get_nodes(edges: Sequence) -> Sequence:
        """
        Returns a list of nodes given a list of edges

        Args:
            edges (Sequence): a list of edges, where an edge is a tuple of nodes

        Returns:
            [Sequence]: a list of nodes in the graph with edges
        """
        nodes = []

        for edge in edges:
            for node in edge:
                if node not in nodes:
                    nodes.append(node)
        return nodes

