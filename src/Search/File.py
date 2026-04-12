import sys
import os
import tracemalloc
import time
from .Algorithms import bfs_res, dfs_res, dls_res, iddfs_res, ucs_res, astar_res, greedy_res, weighted_astar_res
from Controller.Level import level_loader, build_level

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_levels_from_file(input_file):
    levels = []
    current_name = None
    current_bottles = []
    params = {}

    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" in line and not line.startswith("["):
                key, value = line.split(":")
                params[key.strip()] = value.strip()
            elif line.startswith("[") and line.endswith("]"):
                if current_name is not None:
                    levels.append((current_name, current_bottles))
                current_name = line[1:-1]
                current_bottles = []
            else:
                parts = line.split("|")
                colors_part = parts[0].strip()
                capacity = int(parts[1].strip())
                if colors_part == "empty":
                    colors = []
                else:
                    colors = colors_part.split()
                current_bottles.append((colors, capacity))

    if current_name is not None:
        levels.append((current_name, current_bottles))

    return levels, params

def run_all_algorithms_from_file(input_file):
    levels, params = load_levels_from_file(input_file)

    depth_limit = int(params.get("depth_limit", 15))
    max_depth = int(params.get("max_depth", 50))
    weight = float(params.get("weight", 1.5))

    algorithms = [
        ("Breadth First Search", lambda b: bfs_res(b)),
        ("Depth First Search", lambda b: dfs_res(b)),
        ("A* Search", lambda b: astar_res(b)),
        ("Uniform Cost Search", lambda b: ucs_res(b)),
        ("Greedy Search", lambda b: greedy_res(b)),
        ("Iterative Deepening", lambda b: iddfs_res(b, max_depth)),
        ("Depth Limited Search", lambda b: dls_res(b, depth_limit)),
        ("Weighted A*", lambda b: weighted_astar_res(b, weight)),
    ]

    output_dir = os.path.join(BASE_DIR, "output")
    os.makedirs(output_dir, exist_ok=True)
    file_name = os.path.join(output_dir, "output_all.txt")

    with open(file_name, "w") as f:
        sys.stdout = f

        for name, level_data in levels:

            print(f"{'=' * 40}")
            print(f"{name}")
            print(f"{'=' * 40}")
            print()

            for algorithm_name, algorithm_func in algorithms:
                print(f"--- {algorithm_name} ---")
                print()
                bottles = build_level(level_data)
                try:
                    tracemalloc.start()
                    start = time.time()
                    goal = algorithm_func(bottles)
                    elapsed = time.time() - start
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                except Exception as e:
                    print(f"Error: {e}")
                    print()
                    tracemalloc.stop()
                    continue

                if goal is not None:
                    path = []
                    node = goal
                    while node is not None:
                        path.append(node.state)
                        node = node.parent
                    path.reverse()
                    print(f"Solution found in {goal.g} move(s):")
                    print()
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
                print(f"Memory (current): {current / 1024:.2f} KB")
                print(f"Memory (peak): {peak / 1024:.2f} KB")
                print()
    sys.stdout = sys.__stdout__

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
    file_name = os.path.join(output_dir, f"output_{acronym}_{level}.txt")
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

    tracemalloc.start()
    start = time.time()
    goal = algorithm_func(bottles)
    elapsed = time.time() - start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

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
    print(f"Memory (current): {current / 1024:.2f} KB")
    print(f"Memory (peak): {peak / 1024:.2f} KB")
    print()