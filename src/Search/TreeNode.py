class TreeNode:
    def __init__(self, state, parent=None, g=0):
        self.state = state
        self.parent = parent
        self.children = []
        self.g = g

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self