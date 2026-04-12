import sys
import os
import time
from .Algorithms import bfs_res, dfs_res, dls_res, iddfs_res, ucs_res, astar_res, greedy_res, weighted_astar_res
from Controller.Level import level_loader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def print_to_file(algorithm, level, depth_limit, max_depth, weight):

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
    elif algorithm == "Greedy Search":  
        print_to_file_aux(greedy_res, algorithm, "greedy", level)
    elif algorithm == "Weighted A*":
        print_to_file_aux(lambda b: weighted_astar_res(b, weight), algorithm, "w_astar", level)
    

def print_to_file_aux(algorithm_func, algorithm, acronym, level):
    
    output_dir = os.path.join(BASE_DIR, "output")
    file_name = os.path.join(output_dir, f"output_{acronym}.txt")
    os.makedirs(os.path.dirname(file_name), exist_ok=True)


    with open(file_name, "w") as f:
        sys.stdout = f
        print("=" * 40)
        print(f"Algorithm: {algorithm}")
        print(f"Level: {level}")
        print("=" * 40)
        print()

        output_to_file(algorithm_func, level)
    
    sys.stdout = sys.__stdout__
    


def output_to_file(algorithm_func, level):

    bottles = level_loader[level]()

    start = time.time()
    goal = algorithm_func(bottles)
    elapsed = time.time() - start

    if goal is not None:
        print(f"Solution found in {goal.g} move(s):")
        print()
        path = []
        node = goal
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        for step, state in enumerate(path):
            print(f"Step {step}:", end=" ")
            for bottle in state:
                print(bottle, end=" ")
            print()
    else:
        print("No solution found.")

    print()
    print(f"Cost: {goal.g if goal else 'N/A'} move(s)")
    print(f"Time: {elapsed:.4f} seconds")
    print()