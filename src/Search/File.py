import sys
import os
import time
from .Algorithms import bfs_res, dfs_res, astar_res
from Controller.Level import level_loader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def print_to_file(algorithm, num_levels):

    if algorithm == "Breadth First Search":
        print_to_file_aux(bfs_res, algorithm, "bfs", num_levels)
    elif algorithm == "Depth First Search":
        print_to_file_aux(dfs_res, algorithm, "dfs", num_levels)
    elif algorithm == "A* Search":                    
        print_to_file_aux(astar_res, algorithm, "astar", num_levels)


def print_to_file_aux(algorithm_func, algorithm, acronym, num_levels):
    
    output_dir = os.path.join(BASE_DIR, "output")
    file_name = os.path.join(output_dir, f"output_{acronym}.txt")
    os.makedirs(os.path.dirname(file_name), exist_ok=True)


    with open(file_name, "w") as f:
        sys.stdout = f
        print(algorithm)
        print()

        for i in range(1, num_levels + 1):
            output_to_file(algorithm_func, i)
    


def output_to_file(algorithm_func, level):

    print(level)
    bottles = level_loader[level]()

    start = time.time()
    goal = algorithm_func(bottles)
    elapsed = time.time() - start

    print()
    if goal is not None:
        print(f"Cost: {goal.g} move(s)")
    else:
        print("Cost: No solution found")

    print(f"Time: {elapsed:.4f} seconds")
    print()
    
    sys.stdout = sys.__stdout__