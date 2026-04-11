import heapq
from collections import deque
from .TreeNode import TreeNode

from Controller.Controller import check_win, child_bottle_states

def bfs_res(bottles):

    goal = breadth_first_search(bottles, check_win, child_bottle_states)
    print_solution(goal)
    return goal

def dfs_res(bottles):

    goal = depth_first_search(bottles, check_win, child_bottle_states)
    print_solution(goal)
    return goal

def dls_res(bottles, depth_limit):
    
    goal = depth_limited_search(bottles, check_win, child_bottle_states, depth_limit)
    print_solution(goal)
    return goal

def ucs_res(bottles):
    
    goal = uniform_cost_search(bottles, check_win, child_bottle_states)
    print_solution(goal)
    return goal

def iddfs_res(bottles, max_depth):
    
    goal = iterative_deepening_search(bottles, check_win, child_bottle_states, max_depth)
    print_solution(goal)
    return goal

def print_solution(goal):

    if goal is None:
        print("No solution found.")
        return
    
    path = []
    node = goal
    while node is not None:
        path.append(node.state)
        node = node.parent


    path.reverse()

    print(f"Solution found in {len(path) - 1} move(s):")
    print()
    for step, state in enumerate(path):
        print(f"Step {step}:", end=" ")
        for bottle in state:
            print(bottle, end=" ")
        print()

def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    visited = set()
    visited.add(tuple(tuple(b.colors) for b in initial_state))

    while queue:
        node = queue.popleft()   # get first element in the queue
        if goal_state_func(node.state):   # check goal state
            return node

        for state in operators_func(node.state):   # go through next states 
            state_key = tuple(tuple(b.colors) for b in state)
            if state_key not in visited: 
                # é suposto ser state, _ por causa do cost
                visited.add(state_key)

                new_node = TreeNode(state, g=node.g + 1)
                # create tree node with the new state
                # your code here

                node.add_child(new_node)
                # link child node to its parent in the tree
                # your code here

                queue.append(new_node)
                # enqueue the child node
                # your code here


    return None

def depth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    visited = set()
    return depth_first_search_aux(root, goal_state_func, operators_func, visited)


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

def depth_limited_search(initial_state, goal_state_func, operators_func, depth_limit):
    root = TreeNode(initial_state)
    visited = set()
    return dls_aux(root, goal_state_func, operators_func, visited, depth_limit)

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

def iterative_deepening_search(initial_state, goal_state_func, operators_func, max_depth):
    for depth in range(max_depth):
        visited = set()
        root = TreeNode(initial_state)
        result = dls_aux(root, goal_state_func, operators_func, visited, depth)
        if result is not None:
            return result
    return None

# behaves like bfs because every move costs 1
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

# heuristic search strategies

def astar_res(bottles):
    goal = a_star_search(bottles, check_win, child_bottle_states)
    print_solution(goal)
    return goal

def greedy_res(bottles):
    
    goal = greedy_search(bottles, check_win, child_bottle_states)
    print_solution(goal)
    return goal

def weighted_astar_res(bottles, weight):
    
    goal = weighted_astar_search(bottles, check_win, child_bottle_states, weight)
    print_solution(goal)
    return goal

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