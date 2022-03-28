from typing import Dict, List, Tuple
import matplotlib.pyplot as pyplot
import networkx
import numpy

from numpy import random as r

class Graph:
    """ 
    The Graph class allows for the generation of directed graphs containing weights and costs.

    members:
        + edges (List[int]): a list of (from, to) node tuples
        + nodes (List[int]): a list of nodes (sorted in increasing order) in the graph
        + direction_matrix (numpy.ndarray): matrix of the directed edges between nodes
        + networkx_graph (networkx.DiGraph): networkx object representation of graph
    """
    
    def __init__(self, edges: List[int]) -> None:
        """
        Creates a new instance of the Graph class. Initializes the graph's 
        matricies based on the given general matrix.  

        Args:
            edges (Sequence): a list of edges (node from-to tuples)
        """
        self.edges: List[int] = edges
        self.connection_matrix: numpy.ndarray
        self.networkx_graph: networkx.DiGraph
        self.nodes = Graph.get_nodes(self.edges)

        # Initialize connection matrix using the list of edges
        self._initialize_connection_matrix()

        # Initialize the networkx graph
        self._initialize_networkx_graph()

        
    def print_graph(self, picture_name: str = "", edge_labels: Dict[Tuple[int, int], str] | None = None, show_minimal_output: bool = False,
                    highlight_edges = []) -> None:
        """
        Prints the graph using the networkx graph representation and pyplot.

        Args:
            picture_name (str, optional): The name to save the graph image as. Defaults to "".
            edge_labels (Dict[Tuple[int, int], str] | None, optional): The dictionary of edges to labels. Defaults to None.
            suppress_text_output (bool): Supresses print statements and edge labels from being printed on the graph. Defaults to False
        """
        if(not show_minimal_output):
            print("Nodes on Graph:")
            print(f"|    {self.networkx_graph.nodes()}")
            print("Edges of Graph:")
            print(f"|    {self.networkx_graph.edges()}")
            line_width = 8
        else:
            line_width = 4
        
        
        #TODO: Alter size of nodes and lines with size of graph
        networkx.draw_networkx(self.networkx_graph, 
            pos = networkx.circular_layout(self.networkx_graph), node_color = self.get_color_map(len(self.networkx_graph)),
            with_labels = not show_minimal_output, node_size=100 if show_minimal_output else 300, arrows = not show_minimal_output)
        
        if edge_labels and not show_minimal_output:
            networkx.draw_networkx_edge_labels(self.networkx_graph, edge_labels = edge_labels, pos = networkx.circular_layout(self.networkx_graph))

        if len(highlight_edges)>0:
            networkx.draw_networkx_edges(
                self.networkx_graph,
                pos = networkx.circular_layout(self.networkx_graph),
                edgelist=highlight_edges,
                width=line_width,
                alpha=0.5,
                edge_color="tab:red",
                arrows = not show_minimal_output,
            )
            
        if picture_name != "":
            #TODO: Add a parameter to save this in the folder the .py file running the program is in or choice of location
            pyplot.savefig(picture_name) #save as png
            
        pyplot.show() #display

    def get_simple_paths(self, source_node: int | None = None, destination_node: int | None = None) -> List[List[int]]:
        """
        Returns an array of simple paths in the graph

        Args:
            source_node(int): the first node in the path
            destination_node(int): the last node in the path

        Returns:
            List[List[int]]: a list of paths (a path is an array of nodes)
        """
        paths = []

        if source_node is None:
            source_node = self.nodes[0]

        if destination_node is None:
            destination_node = self.nodes[-1]

        if self.networkx_graph and destination_node != source_node:
            paths = [path for path in networkx.all_simple_paths(self.networkx_graph, source_node, destination_node)]

        return paths
    
    def get_color_map(self, n: int, s: int = 0, t: int = -1) -> List[str]:
        """
        Returns a colop mapping for each node in the graph

        Args:
            n (int): the number of nodes
            s (int, optional): The starting node. Defaults to 0.
            t (int, optional): The destination node. Defaults to -1.

        Returns:
            List[str]: a color mapping of each node in the graph
        """
        if t == -1:
            t = n - 1
        else:
             t - 1
        color_map = []
        for i in range(0,n):
            if i == s:
                color_map.append("#00ff44")
            elif i == t:
                color_map.append("#ffff00")
            else:
                color_map.append("#00f2ff")
        return color_map
    
    def get_incoming_nodes(self, node: int) -> List[int]:
        """
        Returns a list of all the nodes directly connected to the given node
        by an incoming edge to the given node.

        Args:
            node (int): the node that is a destination of the incoming edges

        Returns:
            List[int]: a list of nodes (integer identifiers)
        """
        incoming_nodes = []
        # the list of incoming nodes is the corresponding column in the connections matrix
        matrix_column = self.connection_matrix[:, self.nodes.index(node)]
        # add every node with an outgoing edge to the current node
        for i in range(len(matrix_column)):
            if matrix_column[i] != 0:
                incoming_nodes.append(i)
        return incoming_nodes

    def get_outgoing_nodes(self, node: int) -> List[int]:
        """
        Returns a list of all the nodes directly connected to the given node
        by an outgoing edge from the given node.

        Args:
            node (int): the node that is a source of the outgoing edges

        Returns:
            List[int]: a list of nodes (integer identifiers)
        """
        outgoing_nodes = []
        # the list of outoing nodes is the corresponding row in the connections matrix
        matrix_row = self.connection_matrix[self.nodes.index(node), :]
        # add every node with an incoming edge from the current node
        for i in range(len(matrix_row)):
            if matrix_row[i] != 0:
                outgoing_nodes.append(i)
        return outgoing_nodes
    
    def get_con_matrix_element(self, from_node: int, to_node: int) -> int:
        """
        Returns the matrix element M[from_node][to_node]

        Args:
            from_node (int): the origin node of an edge
            to_node (int): the destination node of an edge

        Returns:
            int: the connection matrix element value at that position.
        """
        return self.connection_matrix[self.nodes.index(from_node)][self.nodes.index(to_node)]
    
    def _initialize_networkx_graph(self) -> None:
        """
        Initializes the networkx graph, adding the nodes and edges of the graph 
        to the networkx object.
        """
        self.networkx_graph = networkx.DiGraph()
        # Add nodes
        self.networkx_graph.add_nodes_from(self.nodes)
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

            3x3 Example: list of edges --> [(0, 1), (0, 2)]
                     0  1  2
                 0 [[0, 1, 1],
                 1  [0, 0, 0], 
                 2  [0, 0, 0]]
        """
        # initialize matrix to nxn 0 matrix
        self.connection_matrix = Graph._gen_zero_n_square_matrix(self.edges)

        for edge in self.edges:
            self.connection_matrix[self.nodes.index(edge[0])][self.nodes.index(edge[1])] = 1

    @staticmethod
    def get_nodes(edges: List[Tuple[int, int]]) -> List[int]:
        """
        Returns a list of nodes given a list of edges

        Args:
            edges (Sequence): a list of edges, where an edge is a tuple of nodes

        Returns:
            [List[Tuple[int, int]]]: a list of nodes in the graph with edges
        """
        nodes = []

        for edge in edges:
            for node in edge:
                if node not in nodes:
                    nodes.append(node)
        # sort the nodes
        nodes.sort()
        return nodes

    @staticmethod
    def _gen_zero_n_square_matrix(edges: List[Tuple[int, int]]) -> numpy.ndarray:
        """
        Generates an nxn zero square matrix based on the list of edges

        Args:
            edges (List[Tuple[int, int]]): list of edges in the graph (node pairs)

        Returns:
            numpy.ndarray: an nxn zero square matrix
        """
        nodes = Graph.get_nodes(edges)
        num_nodes = len(nodes)
        return numpy.zeros((num_nodes, num_nodes))

    def get_arbitrary_graph(n: int):
        """Generates arbitrary WC graph with n nodes and no weights or costs

        Args:
            n (int): number of nodes

        Returns:
            Graph: arbitary WC graph with all (w,c) = (0,0)
        """
        graphDict = {}
        #Loop i range(0,n)
        for i in range(0,n-1):
            #Random Noe range(i,n) # of outgoing edges
            N_oe = r.randint(1,n-i) if n-i>1 else 1
            #print("i :", i, "\tN_oe: ", N_oe)
            #Choose Noe unique nodes range(1,n) delta_o[]
            delta_o = r.choice([*range(i+1,n)], N_oe, replace=False) if i!=n-1 else [n]
            #For each j in delta_o[], add edge (i,j)
            for j in delta_o:
                #TODO: Add weights and cost generation -> can only do to a WCGraph
                graphDict[i,j] = (0,0)
            #If no incoming nodes
            oneInNode = False
            for k in range(0,i):
                if((k,i) in graphDict):
                    oneInNode = True
                    break
            if not oneInNode and i != 0:
                #Choose node incoming n_in range(0,i-1)
                n_in = r.randint(0,i-1) if i>1 else 0
                #Add edge (n_in,i)
                #TODO: Add weight and const
                graphDict[n_in,i] = (0,0)
            
        graph = Graph(graphDict)
        return graph

