import sys
import os
import time
from .Algorithms import bfs_res, dfs_res, dls_res, iddfs_res, ucs_res, astar_res
from Controller.Level import level_loader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def print_to_file(algorithm, level, depth_limit, max_depth):

    if algorithm == "Breadth First Search":
        print_to_file_aux(bfs_res, algorithm, "bfs", level)
    elif algorithm == "Depth First Search":
        print_to_file_aux(dfs_res, algorithm, "dfs", level)
    elif algorithm == "Depth Limited Search":
        print_to_file_aux(lambda b: dls_res(b, depth_limit), algorithm, "dls", level)
    elif algorithm == "Iterative Deepening":
        print_to_file_aux(lambda b: iddfs_res(b, max_depth), algorithm, "iddfs", level)
    elif algorithm == "Uniform Cost":
        print_to_file_aux(ucs_res, algorithm, "ucs", level)
    elif algorithm == "A* Search":  
        print_to_file_aux(astar_res, algorithm, "astar", level)


def print_to_file_aux(algorithm_func, algorithm, acronym, level):
    
    output_dir = os.path.join(BASE_DIR, "output")
    file_name = os.path.join(output_dir, f"output_{acronym}.txt")
    os.makedirs(os.path.dirname(file_name), exist_ok=True)


    with open(file_name, "a") as f:
        sys.stdout = f
        print(algorithm)
        print()

        output_to_file(algorithm_func, level)
    


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