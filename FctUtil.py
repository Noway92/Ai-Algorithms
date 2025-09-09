import heapq
import functools
import numpy as np


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. """

    def __init__(self, state, parent=None, action=None, path_cost= 1):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.path_cost < node.path_cost
    
    
    def __len__(self):
        return 0 if self.parent is None else (1+len(self.parent))
    
    
    def expand(self, problem,f,heuristics):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, move_allowed,f,heuristics) for move_allowed in problem.move_allowed(self.state)]

    def child_node(self, problem, move_allowed,f,heuristics):
        next_state = problem.result(self.state, move_allowed)
        # 3 possibilities : 
        # the first one is fot UCS
        if(heuristics==None and f!=None):next_node = Node(next_state, self, move_allowed,f(self.path_cost))
        # The second one is for BFS using heuristics
        elif(heuristics != None and f==None):next_node = Node(next_state, self, move_allowed,path_cost=heuristics(next_state))
        # The third one is for A_star
        elif(heuristics!=None and f !=None):next_node = Node(next_state, self, move_allowed,path_cost=heuristics(next_state)+f(self.path_cost)-heuristics(self.state)) 
        return next_node
    

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


    def __eq__(self, other):
        if isinstance(self.state, np.ndarray) and isinstance(other.state, np.ndarray):
            return np.array_equal(self.state, other.state)
        return self.state == other.state
    
    # It's allowing the node to be hasshable (because initially the state is not)
    def __hash__(self):
        return hash(hashable_array(self.state))


# Its the same Class that is in the notebook 
class EightPuzzle:
    def __init__(self):
        #Initial state (we can initialise our matric with it)
        self.initial_state=np.array([[7,2,4],[5,-1,6],[8,3,1]])
        self.goal_state=np.array([[-1,1,2],[3,4,5],[6,7,8]])
    
    @property
    def Initial_State(self):
        return self.initial_state

    @property
    def Goal_State(self):
        return self.goal_state

    #By actions we mean that the empty(here -1) case go up or down ...
    def move(self,action,state):
        new_state = state.copy()
        row, col =np.where(state==-1)
        if(action=="up"):
            new_state[row, col], new_state[row - 1, col] = new_state[row - 1, col], new_state[row, col]
        elif(action=="down"):
            new_state[row, col], new_state[row + 1, col] = new_state[row + 1, col], new_state[row, col]
        elif(action=="left"):
            new_state[row, col], new_state[row, col -1] = new_state[row, col-1], new_state[row, col]
        elif(action=="right"):
            new_state[row, col], new_state[row, col +1] = new_state[row, col+1], new_state[row, col]

        return new_state

    def move_allowed(self,state):
        tab_actions = []  # List to tell which actions are allowed from your node
        row, col = np.where(state == -1)
        row, col = row[0], col[0]  # obtain the scalar indices
        if row != 0:tab_actions.append("up")
        if col != 2:tab_actions.append("right")
        if row != 2:tab_actions.append("down")
        if col != 0:tab_actions.append("left")
        return np.array(tab_actions)  # Transform the list in a numpy array

    # Fonction that tells you if you reach the goal or not
    def GoalReach(self,state):
        #This is the Goal Matrix
        return np.array_equal(state,self.goal_state)

    def result(self,state,move):
        return self.move(move, state)

# Function allowing the numpy array to be transorm into a tuple.
# It's useful because otherwise it's not hasshable  
def hashable_array(arr):
    return tuple(arr.flatten()) if isinstance(arr, np.ndarray) else tuple(arr)