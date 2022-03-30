import json
import matplotlib.pyplot as plt
import numpy
import os

from time import time, localtime, asctime
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

    figure, axis = plt.subplots(2)

    figure.suptitle("Label Setting Benchmarking")

    axis[0].scatter(results.keys(), results.values(), marker = ".")
    axis[0].set(xlabel = "graph size (number of nodes)")
    axis[0].set(ylabel = "time (s)")

    axis[1].scatter(results.keys(), results.values(), marker = ".")
    axis[1].set(xlabel = "graph size (number of nodes)")
    axis[1].set(ylabel = "time (ln(s))")
    axis[1].set_yscale("log", base = numpy.e)
    axis[1].set_yticklabels(["$%.3f$" % y for y in results.values()])
    
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

def save_data(file_name, data):
    if input("Save plot data (y/n)? ") == 'y':
        with open(file_name, "w") as file:
            json.dump(data, file)

def main():

    results = {}
    response = input("Load existing plot?(y/n): ")
    if (response == 'y'):
        results = load_data(input("Enter file path: "))
        plot_results(results)
    else:
        try:
            graph_sizes = [ 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 
                            100, 110, 120, 130, 140, 150, 160, 170, 180, 190,
                            200, 225, 250, 275, 300, 325, 350, 375, 400, 500]
            LabelAlgorithmBase.suppress_output = True
            for graph_size in graph_sizes:
                print(f"Running graph with {graph_size} nodes...")
                graph: WCGraph = WCGraph.get_arbitrary_graph(n = graph_size, mean_weight = 3, mean_cost = 3, peak = graph_size)  
                labels: LabelAlgorithmRec = LabelAlgorithmRec()

                labels.min_percent_remain = 0.99

                runtime = time_function(lambda: labels.run_algorithm(graph, source_node = 0, max_weight = graph_size))
                results[graph_size] = runtime
        except:
            print("Ended early.")
        finally:
            time_str = "".join("-".join(asctime(localtime()).split(' ')).split(':'))
            graph_range_str = f"{graph_sizes[0]}-{graph_sizes[-1]}"
            filename = f"resources/Bench/LabelSetting/data_{graph_range_str}_{time_str}.json"
            save_data(filename, results)
            print_results(results)
            plot_results(results)
    








    

if __name__ == "__main__":
    main()