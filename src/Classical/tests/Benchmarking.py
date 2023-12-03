import json
from multiprocessing.sharedctypes import Value
import matplotlib.pyplot as plt
import numpy
import os
from scipy import optimize

from time import time, localtime, asctime
from typing import Callable, Dict

from src.GraphModeling.models.WCGraph import WCGraph
from src.LabelSetting.models.LabelAlgorithmBase import LabelAlgorithmBase
from src.LabelSetting.models.LabelAlgorithmRec import LabelAlgorithmRec

# GLOBAL VARIABLE (I was lazy...)
MAX_WEIGHT = 500

def time_function(function: Callable, clear_output: bool = False) -> float:
    """
    Calculates the time it takes for a given function to run.

    Args:
        function (Callable): the function to time
        clear_output (bool, optional): option to clear the termainl after running the function. Defaults to False.

    Returns:
        float: the total time it took to run the function in seconds.
    """
    start_time = time()
    function()
    end_time = time()
    
    if clear_output: os.system('cls||clear')  # clear terminal output

    return end_time - start_time

def best_fit(x):
    # hardcoded best fit from sci-davis
    a = 0.0102148891261219
    b = 1.20132852815925
    c = 1.39861309009397
    return b * numpy.exp(x * a + c)

def theoretical(x, a, b, c):
    # hardcoded scaling 
    # a = 0.0161685375
    # a = 0.00909806085390579
    # b = 8.35286636705807
    return b * numpy.exp(x * a + c)

def Big_O(num_edges, max_weight, a, b):
    # a = 0.000005
    return a * num_edges * max_weight + b

def plot_results(node_results: Dict[int, float], edge_results: Dict[int, float]):

    figure, (node_axii, edge_axii) = plt.subplots(2, 2)

    figure.suptitle("Label Setting Benchmarking")

    node_axii[0].scatter(node_results.keys(), node_results.values(), marker = ".")
    node_axii[0].set(xlabel = "graph size (number of nodes)")
    node_axii[0].set(ylabel = "time (s)")

    node_axii[1].scatter(node_results.keys(), node_results.values(), marker = ".")
    node_axii[1].set(xlabel = "graph size (number of nodes)")
    node_axii[1].set(ylabel = "time (ln(s))")
    node_axii[1].set_yscale("log", base = numpy.e)
    node_axii[1].set_yticklabels(["$%.3f$" % y for y in node_results.values()])

    edge_axii[0].scatter(edge_results.keys(), edge_results.values(), marker = ".")
    edge_axii[0].set(xlabel = "graph complexity (number of edges)")
    edge_axii[0].set(ylabel = "time (s)")

    edge_axii[1].scatter(edge_results.keys(), edge_results.values(), marker = ".")
    edge_axii[1].set(xlabel = "graph complexity (number of edges)")
    edge_axii[1].set(ylabel = "time (ln(s))")
    edge_axii[1].set_yscale("log", base = numpy.e)
    edge_axii[1].set_yticklabels(["$%.3f$" % y for y in node_results.values()])

    # calculates the scaling factors for the theoretical plot based on the best fit line
    x = [key for key in node_results.keys()]
    y = [value for value in node_results.values()]
    results = optimize.curve_fit(theoretical,  x,  y,  p0=(0.001, 1, -1))
    a = results[0][0]
    b = results[0][1]
    c = results[0][2]

    print(f"a = {a}\nb = {b}\nc = {c}")

    for axis in node_axii:
        x_limit = axis.get_xlim()
        y_limit = axis.get_ylim()
        x_axis = range(int(x_limit[0]), int(x_limit[1]))      
        # ax.plot( x_axis, [ best_fit(x) for x in x_axis ], 'r:' )

        axis.plot( x_axis, [ theoretical(x, a, b, c) for x in x_axis ], 'g:' )
        axis.set_xlim(x_limit) 
        axis.set_ylim(y_limit)
    
    # calculates the scaling factors for the theoretical plot based on the best fit line
    x = [key for key in edge_results.keys()]
    y = [value for value in edge_results.values()]
    results = optimize.curve_fit(lambda x,a: MAX_WEIGHT * a * x,  x,  y)
    a = results[0][0]

    # a, b = numpy.polyfit(x, y, 1)

    print(f"\na = {a}")

    for axis in edge_axii:
        x_limit = axis.get_xlim()
        y_limit = axis.get_ylim()
        x_axis = range(int(x_limit[0]), int(x_limit[1]))      

        y_axis = []
        for i in range(len(x_axis)):
            y_axis.append(Big_O(x_axis[i], MAX_WEIGHT, a, b = 0))
        axis.plot( x_axis, y_axis, 'g:' )

        axis.set_xlim(x_limit) 
        axis.set_ylim(y_limit)
    
    plt.show()


def print_results(results: Dict[int, float]):
    print()
    for graph_size, time in results.items():
        print(f"{graph_size}: {time} seconds")

def load_data(file_name):
    results = {}
    with open(file_name, "r") as file:
        json_obj = json.load(file)
    for x in json_obj:
        results[int(x)] = json_obj[x]
    return results

def load_all_data(folder_path):
    node_data = {}
    edge_data = {}

    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.startswith("node"):
                node_data = load_data(f"{folder_path}/{file}")
            elif file.startswith("edge"):
                edge_data = load_data(f"{folder_path}/{file}")
    else:
        print("Error: Folder path does not exist.")

    return node_data, edge_data

def generate_file_names(time_str, node_range_str, edge_range_str):
    folder = f"resources/Bench/LabelSetting/{time_str}/"
    filename_node = f"{folder}node_data_{node_range_str}.json"
    filename_edge = f"{folder}edge_data_{edge_range_str}.json"

    if not os.path.isdir(f"resources/Bench/LabelSetting/{time_str}/"):
        os.mkdir(folder)

    return filename_node, filename_edge

def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file)

def save_all_data(node_results: Dict[int, float], edge_results: Dict[int, float]):
    time_str = "".join("-".join(asctime(localtime()).split(' ')).split(':'))
    graph_sizes_nodes = [key for key in node_results.keys()]
    graph_sizes_edges = [key for key in node_results.keys()]
    node_range_str = f"{graph_sizes_nodes[0]}-{graph_sizes_nodes[-1]}"
    edge_range_str = f"{graph_sizes_edges[0]}-{graph_sizes_edges[-1]}"

    filename_node, filename_edge = generate_file_names(time_str, node_range_str, edge_range_str)

    save_data(filename_node, node_results)
    save_data(filename_edge, edge_results)

def main():

    node_results = {}
    edge_results = {}
    response = input("Load existing plot?(y/n): ")
    if (response == 'y'):
        response = input("Load individual files (1) or a folder (2)?: ")
        if response == "1":
            node_file = input("Enter file path for nodes: ")
            edge_file = input("Enter file path for edges: ")
            if node_file != "":
                node_results = load_data(node_file)
            if edge_file != "":
                edge_results = load_data(edge_file)
        else:
            folder_path = input("Enter folder path: ")
            node_results, edge_results = load_all_data(folder_path)
        plot_results(node_results, edge_results)
    else:
        try:
            graph_sizes = [ 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 
                            100, 110, 120, 130, 140, 150, 160, 170, 180, 190,
                            200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500]
            LabelAlgorithmBase.suppress_output = True
            for graph_size in graph_sizes:
                print(f"Running graph with {graph_size} nodes...")
                graph: WCGraph = WCGraph.get_arbitrary_graph(n = graph_size, mean_weight = 3, mean_cost = 3, peak = graph_size)  
                labels: LabelAlgorithmRec = LabelAlgorithmRec()

                labels.min_percent_remain = 0.99

                runtime = time_function(lambda: labels.run_algorithm(graph, source_node = 0, max_weight = MAX_WEIGHT))
                node_results[graph_size] = runtime
                edge_results[len(graph.edges)] = runtime
        except:
            print("Ended early.")
        finally:
            if input("Save plot data (y/n)? ") == "y":
                save_all_data(node_results, edge_results)
            print_results(node_results)
            plot_results(node_results, edge_results)
    
if __name__ == "__main__":
    main()