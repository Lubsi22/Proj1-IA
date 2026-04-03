import sys
from .Algorithms import bfs_res, dfs_res
from Controller.Level import level_loader

def print_to_file(algorithm, num_levels):

    if algorithm == "Breadth First Search":
        print_to_file_aux(bfs_res, algorithm, "bfs", num_levels)
    elif algorithm == "Depth First Search":
        print_to_file_aux(dfs_res, algorithm, "dfs", num_levels)


def print_to_file_aux(algorithm_func, algorithm, acronym, num_levels):
    
    file_name = "Search/output/output_" + acronym + ".txt"
    with open(file_name, "w") as f:
        sys.stdout = f
        print(algorithm)
        print()

        for i in range(1, num_levels + 1):
            output_to_file(algorithm_func, i)
    
        print()
        print("Final results: .......")


def output_to_file(algorithm_func, level):

    print(level)
    bottles = level_loader[level]()
    algorithm_func(bottles)
    print()
    print("Cost: ...")
    print("Time: ...")
    print("Memory: ...")
        