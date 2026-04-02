from collections import deque
from .TreeNode import TreeNode

from Controller.Controller import check_win, child_bottle_states

def test_bfs(bottles):

    goal = breadth_first_search(bottles, check_win, child_bottle_states)
    print_solution(goal)

def test_dfs(bottles):

    goal = depth_first_search(bottles, check_win, child_bottle_states)
    print_solution(goal)

def print_solution(goal):

    if (goal != None):
        for g in goal.state:
            print(g, end=' ')
        print('')
        return print_solution(goal.parent)
    return

    '''
    for g in goal.state:
        print(g, end=' ')
    print('')
    #print(goal.state)
    '''

def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes

    while queue:
        node = queue.popleft()   # get first element in the queue
        if goal_state_func(node.state):   # check goal state
            return node

        for state in operators_func(node.state):   # go through next states 

            # é suposto ser state, _ por causa do cost

            new_node = TreeNode(state)
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
    visited = []
    return depth_first_search_aux(root, goal_state_func, operators_func, visited)


def depth_first_search_aux(node, goal_state_func, operators_func, visited):
    visited.append(node.state)

    if goal_state_func(node.state):
        return node

    for state in operators_func(node.state): # state, _
        new_node = TreeNode(state)
        if new_node.state not in visited:
            node.add_child(new_node)
            return depth_first_search_aux(new_node, goal_state_func, operators_func, visited)

    return None