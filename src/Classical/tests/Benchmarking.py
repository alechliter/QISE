from time import time
from unittest import result
import matplotlib.pyplot as plt
import os

from typing import Callable, Dict

from src.GraphModeling.models.WCGraph import WCGraph
from src.LabelSetting.models.LabelAlgorithmBase import LabelAlgorithmBase
from src.LabelSetting.models.LabelAlgorithmRec import LabelAlgorithmRec

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

def plot_results(results: Dict[int, float]):
    plt.scatter(results.keys(), results.values(), marker = ".")
    plt.xlabel("graph size (number of nodes)")
    plt.ylabel("time (s)")
    plt.show()

def print_results(results: Dict[int, float]):
    print()
    for graph_size, time in results.items():
        print(f"{graph_size}: {time} seconds")

def main():

    graph_sizes = [5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 400, 500]
    results = {}

    LabelAlgorithmBase.suppress_output = True
    try:
        for graph_size in graph_sizes:
            print(f"Running graph with {graph_size} nodes...")
            graph: WCGraph = WCGraph.get_arbitrary_graph(n = graph_size, mean_weight = 3, mean_cost = 3, peak = graph_size)  
            labels: LabelAlgorithmRec = LabelAlgorithmRec()

            labels.min_percent_remain = 0.9

            runtime = time_function(lambda: labels.run_algorithm(graph, source_node = 0, max_weight = graph_size))
            results[graph_size] = runtime
    except:
        print("Ended early.")
    finally:
        print_results(results)
        plot_results(results)
    

if __name__ == "__main__":
    main()