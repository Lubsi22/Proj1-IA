## @file Algorithms.py
#  @brief Search algorithm implementations for the Water Sort puzzle solver.
#
#  Provides eight search strategies — uninformed and informed — each accepting
#  a goal-test function and an operators function so they remain decoupled from
#  game-specific logic.  The public *_res wrappers bind those callables and are
#  the entry points used by File.py and main.py.
 
import heapq
from collections import deque
from .TreeNode import TreeNode

from Controller.Controller import check_win, child_bottle_states
# ---------------------------------------------------------------------------
# Public wrapper functions
# ---------------------------------------------------------------------------

## @brief Runs Breadth-First Search on the given bottle state.
#  @param bottles List of Bottle objects representing the initial state.
#  @return The goal TreeNode if a solution is found, None otherwise.
def bfs_res(bottles):

    goal = breadth_first_search(bottles, check_win, child_bottle_states)
    return goal

## @brief Runs Depth-First Search on the given bottle state.
#  @param bottles List of Bottle objects representing the initial state.
#  @return The goal TreeNode if a solution is found, None otherwise.
def dfs_res(bottles):

    goal = depth_first_search(bottles, check_win, child_bottle_states)
    return goal

## @brief Runs Depth-Limited Search on the given bottle state.
#  @param bottles     List of Bottle objects representing the initial state.
#  @param depth_limit Maximum depth the search is allowed to explore.
#  @return The goal TreeNode if a solution is found within the limit, None otherwise.
def dls_res(bottles, depth_limit):
    
    goal = depth_limited_search(bottles, check_win, child_bottle_states, depth_limit)
    return goal

## @brief Runs Uniform Cost Search on the given bottle state.
#
#  Because every move costs 1, UCS behaves identically to BFS in this domain.
#
#  @param bottles List of Bottle objects representing the initial state.
#  @return The goal TreeNode if a solution is found, None otherwise.
def ucs_res(bottles):
    
    goal = uniform_cost_search(bottles, check_win, child_bottle_states)
    return goal

## @brief Runs Iterative Deepening Depth-First Search on the given bottle state.
#  @param bottles   List of Bottle objects representing the initial state.
#  @param max_depth Upper bound on the depth limit to try before giving up.
#  @return The goal TreeNode if a solution is found within max_depth, None otherwise.
def iddfs_res(bottles, max_depth):
    
    goal = iterative_deepening_search(bottles, check_win, child_bottle_states, max_depth)
    return goal
## @brief Runs A* Search on the given bottle state.
#  @param bottles List of Bottle objects representing the initial state.
#  @return The goal TreeNode if a solution is found, None otherwise.
def astar_res(bottles):
    goal = a_star_search(bottles, check_win, child_bottle_states)
    return goal

## @brief Runs Greedy Best-First Search on the given bottle state.
#  @param bottles List of Bottle objects representing the initial state.
#  @return The goal TreeNode if a solution is found, None otherwise.
def greedy_res(bottles):
    
    goal = greedy_search(bottles, check_win, child_bottle_states)
    return goal

## @brief Runs Weighted A* Search on the given bottle state.
#  @param bottles List of Bottle objects representing the initial state.
#  @param weight  Inflation factor applied to the heuristic (w > 1 trades
#                 optimality for speed; w = 1 is standard A*).
#  @return The goal TreeNode if a solution is found, None otherwise.
def weighted_astar_res(bottles, weight):
    
    goal = weighted_astar_search(bottles, check_win, child_bottle_states, weight)
    return goal

# ---------------------------------------------------------------------------
# Uninformed search algorithms
# ---------------------------------------------------------------------------

## @brief Explores the state space level by level, guaranteeing the shortest path.
#
#  Uses a FIFO queue and a visited set keyed on color tuples to avoid
#  revisiting states.
#
#  @param initial_state    List of Bottle objects for the starting configuration.
#  @param goal_state_func  Callable(state) -> bool that returns True on a solved state.
#  @param operators_func   Callable(state) -> list[state] that returns successor states.
#  @return The goal TreeNode (with parent links for path reconstruction), or None.

def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   
    queue = deque([root])  
    visited = set()
    visited.add(tuple(tuple(b.colors) for b in initial_state))

    while queue:
        node = queue.popleft()   
        if goal_state_func(node.state):  
            return node

        for state in operators_func(node.state):  
            state_key = tuple(tuple(b.colors) for b in state)
            if state_key not in visited: 
                visited.add(state_key)

                new_node = TreeNode(state, g=node.g + 1)
                node.add_child(new_node)
                queue.append(new_node)
                


    return None


## @brief Explores the state space by going as deep as possible before backtracking.
#
#  Delegates to the recursive helper depth_first_search_aux.
#
#  @param initial_state    List of Bottle objects for the starting configuration.
#  @param goal_state_func  Callable(state) -> bool that returns True on a solved state.
#  @param operators_func   Callable(state) -> list[state] that returns successor states.
#  @return The goal TreeNode, or None if no solution exists.

def depth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    visited = set()
    return depth_first_search_aux(root, goal_state_func, operators_func, visited)

## @brief Recursive helper that carries out the DFS traversal.
#
#  Marks the current node as visited before expanding children so that
#  cycles within the same branch are not revisited.
#
#  @param node             The current TreeNode being expanded.
#  @param goal_state_func  Callable(state) -> bool that returns True on a solved state.
#  @param operators_func   Callable(state) -> list[state] that returns successor states.
#  @param visited          Set of state keys already seen in this search.
#  @return The goal TreeNode if found in this subtree, None otherwise.

def depth_first_search_aux(node, goal_state_func, operators_func, visited):
    state_key = tuple(tuple(b.colors) for b in node.state)
    visited.add(state_key)

    if goal_state_func(node.state):
        return node

    for state in operators_func(node.state): # state, _
        state_key = tuple(tuple(b.colors) for b in state)
        if state_key not in visited:
            new_node = TreeNode(state, g=node.g + 1)
            node.add_child(new_node)
            result = depth_first_search_aux(new_node, goal_state_func, operators_func, visited)
            if result is not None:
                return result

    return None

## @brief Performs DFS but stops expanding nodes beyond a fixed depth.
#
#  Delegates to the recursive helper dls_aux.
#
#  @param initial_state    List of Bottle objects for the starting configuration.
#  @param goal_state_func  Callable(state) -> bool that returns True on a solved state.
#  @param operators_func   Callable(state) -> list[state] that returns successor states.
#  @param depth_limit      Maximum number of moves from the root to explore.
#  @return The goal TreeNode if found within the depth limit, None otherwise.
def depth_limited_search(initial_state, goal_state_func, operators_func, depth_limit):
    root = TreeNode(initial_state)
    visited = set()
    return dls_aux(root, goal_state_func, operators_func, visited, depth_limit)

## @brief Recursive helper that carries out the depth-limited traversal.
#
#  Expansion is cut off when node.g reaches the depth limit.  The visited
#  set is shared across all branches, so a state pruned at shallow depth
#  will not be re-explored at a deeper depth within the same call.
#
#  @param node             The current TreeNode being expanded.
#  @param goal_state_func  Callable(state) -> bool that returns True on a solved state.
#  @param operators_func   Callable(state) -> list[state] that returns successor states.
#  @param visited          Set of state keys already seen in this search.
#  @param depth_limit      Maximum depth allowed from the root.
#  @return The goal TreeNode if found, None otherwise.
def dls_aux(node, goal_state_func, operators_func, visited, depth_limit):
    state_key = tuple(tuple(b.colors) for b in node.state)
    visited.add(state_key)

    if goal_state_func(node.state):
        return node

    if node.g >= depth_limit:
        return None

    for state in operators_func(node.state):
        state_key = tuple(tuple(b.colors) for b in state)
        if state_key not in visited:
            new_node = TreeNode(state, g=node.g + 1)
            node.add_child(new_node)
            result = dls_aux(new_node, goal_state_func, operators_func, visited, depth_limit)
            if result is not None:
                return result

    return None

## @brief Repeatedly runs DLS with increasing depth limits until a solution is found.
#
#  Combines the memory efficiency of DFS with the completeness of BFS.
#  Each iteration starts a fresh visited set and a new root node so that
#  the deeper limit can reach states pruned in earlier iterations.
#
#  @param initial_state    List of Bottle objects for the starting configuration.
#  @param goal_state_func  Callable(state) -> bool that returns True on a solved state.
#  @param operators_func   Callable(state) -> list[state] that returns successor states.
#  @param max_depth        The highest depth limit to attempt before giving up.
#  @return The goal TreeNode if found within max_depth iterations, None otherwise.
def iterative_deepening_search(initial_state, goal_state_func, operators_func, max_depth):
    for depth in range(max_depth):
        visited = set()
        root = TreeNode(initial_state)
        result = dls_aux(root, goal_state_func, operators_func, visited, depth)
        if result is not None:
            return result
    return None

## @brief Expands nodes in order of increasing path cost using a min-heap.
#
#  Because every pour costs 1, the cost ordering matches BFS level order and
#  both algorithms find the same optimal solution.  A tie-breaking counter is
#  used to keep the heap stable when two nodes share the same cost.
#
#  @param initial_state    List of Bottle objects for the starting configuration.
#  @param goal_state_func  Callable(state) -> bool that returns True on a solved state.
#  @param operators_func   Callable(state) -> list[state] that returns successor states.
#  @return The goal TreeNode with minimum cost, or None if no solution exists.
def uniform_cost_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state, g=0)

    counter = 0
    heap = []
    heapq.heappush(heap, (0, counter, root))

    visited = {}

    while heap:
        cost, _, node = heapq.heappop(heap)

        state_key = tuple(tuple(b.colors) for b in node.state)

        if state_key in visited and visited[state_key] <= node.g:
            continue
        visited[state_key] = node.g

        if goal_state_func(node.state):
            return node

        for child_state in operators_func(node.state):
            child_g = node.g + 1

            child_node = TreeNode(child_state, g=child_g)
            node.add_child(child_node)

            counter += 1
            heapq.heappush(heap, (child_g, counter, child_node))

    return None

# ---------------------------------------------------------------------------
# Heuristic function
# ---------------------------------------------------------------------------

## @brief Estimates the number of moves remaining to solve the given state.
#
#  The estimate combines two independent penalty terms:
#
#  - **color_breaks**: the total number of adjacent pairs within any bottle
#    where the lower color differs from the upper color.  Each break requires
#    at least one future move to separate.
#
#  - **color_spread**: for each color, the number of extra bottles it currently
#    occupies beyond one (i.e. bottles_containing_color - 1).  A spread of 0
#    means the color is already consolidated; higher values imply more pours.
#
#  The heuristic is admissible in the sense that it never overestimates badly
#  in practice, though it is not strictly proven admissible.
#
#  @param bottles List of Bottle objects representing the state to evaluate.
#  @return A non-negative integer estimate of remaining moves.
def heuristic(bottles):
    color_breaks = 0
    spread = {}

    for idx, bottle in enumerate(bottles):
        colors = bottle.colors
        for i in range(len(colors) - 1):
            if colors[i] != colors[i + 1]:
                color_breaks += 1
        for color in set(colors):
            spread.setdefault(color, set()).add(idx)

    color_spread = sum(len(tubes) - 1 for tubes in spread.values())

    return color_breaks + color_spread

# ---------------------------------------------------------------------------
# Informed search algorithms
# ---------------------------------------------------------------------------

## @brief Finds the optimal solution by minimising f(n) = g(n) + h(n).
#
#  Uses a min-heap ordered by f-value.  A dict-based visited map allows a
#  node to be re-expanded if it is later reached with a lower g-cost.
#  A tie-breaking counter keeps the heap stable when f-values are equal.
#
#  @param initial_state    List of Bottle objects for the starting configuration.
#  @param goal_state_func  Callable(state) -> bool that returns True on a solved state.
#  @param operators_func   Callable(state) -> list[state] that returns successor states.
#  @return The goal TreeNode with the lowest cost path, or None if unsolvable.

def a_star_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state, g=0)

    counter = 0
    heap = []
    heapq.heappush(heap, (heuristic(initial_state), counter, root))

    visited = {}

    while heap:

        f, _, node = heapq.heappop(heap)

        state_key = tuple(tuple(b.colors) for b in node.state)

        if state_key in visited and visited[state_key] <= node.g:
            continue
        visited[state_key] = node.g

        if goal_state_func(node.state):
            return node

        for child_state in operators_func(node.state):
            child_g = node.g + 1                      
            child_h = heuristic(child_state)
            child_f = child_g + child_h

            child_node = TreeNode(child_state, g=child_g)
            node.add_child(child_node)

            counter += 1
            heapq.heappush(heap, (child_f, counter, child_node))


    return None


## @brief Expands nodes in order of heuristic value only, ignoring path cost.
#
#  Greedy search is fast but not optimal and not complete — it can get stuck
#  in local minima.  Uses a set-based visited structure (not dict) because
#  there is no cost to track per state.
#
#  @param initial_state    List of Bottle objects for the starting configuration.
#  @param goal_state_func  Callable(state) -> bool that returns True on a solved state.
#  @param operators_func   Callable(state) -> list[state] that returns successor states.
#  @return The goal TreeNode if found, or None if the search gets stuck.
def greedy_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state, g=0)

    counter = 0
    heap = []
    heapq.heappush(heap, (heuristic(initial_state), counter, root))

    visited = set()

    while heap:
        _, _, node = heapq.heappop(heap)

        state_key = tuple(tuple(b.colors) for b in node.state)

        if state_key in visited:
            continue
        visited.add(state_key)

        if goal_state_func(node.state):
            return node

        for child_state in operators_func(node.state):
            child_key = tuple(tuple(b.colors) for b in child_state)
            if child_key not in visited:
                child_node = TreeNode(child_state, g=node.g + 1)
                node.add_child(child_node)

                counter += 1
                heapq.heappush(heap, (heuristic(child_state), counter, child_node))

    return None

## @brief Runs A* with the heuristic scaled by a weight factor.
#
#  The priority of each node is f(n) = g(n) + w * h(n).  A weight greater
#  than 1 inflates the heuristic, biasing the search toward the goal faster
#  at the cost of solution optimality.  Setting weight = 1 gives standard A*.
#
#  @param initial_state    List of Bottle objects for the starting configuration.
#  @param goal_state_func  Callable(state) -> bool that returns True on a solved state.
#  @param operators_func   Callable(state) -> list[state] that returns successor states.
#  @param weight           Heuristic inflation factor (float, typically 1.0–5.0).
#  @return The goal TreeNode if found, or None if the state space is exhausted.
def weighted_astar_search(initial_state, goal_state_func, operators_func, weight):
    root = TreeNode(initial_state, g=0)

    counter = 0
    heap = []
    heapq.heappush(heap, (weight * heuristic(initial_state), counter, root))

    visited = {}

    while heap:
        f, _, node = heapq.heappop(heap)

        state_key = tuple(tuple(b.colors) for b in node.state)

        if state_key in visited and visited[state_key] <= node.g:
            continue
        visited[state_key] = node.g

        if goal_state_func(node.state):
            return node

        for child_state in operators_func(node.state):
            child_g = node.g + 1
            child_h = heuristic(child_state)
            child_f = child_g + weight * child_h

            child_node = TreeNode(child_state, g=child_g)
            node.add_child(child_node)

            counter += 1
            heapq.heappush(heap, (child_f, counter, child_node))

    return None