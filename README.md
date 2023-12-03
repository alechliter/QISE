# Intro
The goal of this project is to benchmark an existing shortest path algorithm for the a weight-constrained graph and evaluate a possible solution using quantum computing. The original implementation was slow and difficult to read. This version aims to implement the original goal of the project in a simple easy-to-read format.
# Weight Constrained Graph
The weight constrained graph problem posits that you have nodes with both a cost and a weight. You are trying to find the path from node a to node b with a minimal cost while being under a total weight W.
# Lagrangian Relaxation
The algorithm used to solve this problem classically is called "Lagrangian relaxation". Since it is difficult to evaluate each path's cost and weight, cost and weight are simplified into a single value cost_weight by specifying a value alpha. 

weight_cost = cost + alpha\*weight

We can then apply an existing algorithm that solves the minimum path of a cost graph to find the minimum path of the weight constrained graph.
# Implementation
We use the networkx package to generate example graphs and solve the weight_cost graph using the in-build shortest_path() method. Paths are generated using generate_graphs.py and are benchmarked in main.py.
