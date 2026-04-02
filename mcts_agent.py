import math
import random

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state=state #here the game state will be stored
        self.parent= parent#this is for the parent node in the search tree
        self.move= move#used to store the mvoe used to reach the node from its parent
        self.children=[]#all children in node
        self.visits= 0#number of time the node has been visited
        self.total_points= state.get_legal_moves()#amount fo points total

    def is_terminal(self):
        return self.state.is_terminal()#true if node state is terminal
    def fully_expanded(self):#true if there is no more unexplored moves
        return len(self.untried_moves)==0
    def best_child(self, c=math.sqrt(2)):#selects the child with the highest UCT score
        best_score= float("-inf")
        best_node= None

        for child in self.children:
            if child.visits==0:
                score=float("inf")
            else:
                exploitation= child.total_points / child.visits#average amount of points for this child
                exploration= c * math.sqrt(math.log(self.visits) / child.visits)#tries children that have not been visited as much
                score = exploitation + exploration#UCT Score
            if score > best_score:
                best_score = score
                best_node = child
        return best_node
    def expand(self):
        move= random.choice(self.untried_moves)#chooses one unexplored move randomly
        self.untried_moves.remove(move)

        next_state= self.make_move(move)#generates the next game state from that move

        child_node= MCTSNode(next_state, parent=self, move=move)#create a new child node
        self.children.append(child_node)
        return child_node
    
def simulate_random_play(state,root_player):
    current_state= state#starts at the given state

    while not current_state.is_terminal():#makes random legal move until the game ends
        move= random.choice(current_state.get_legal_moves())
        current_state= current_state.make_move(move)
    result= current_state.utility()

    if result==root_player:
        return 1
    elif result==0:
        return 0
    else:
        return -1
        
def backpropagate(node, reward):
    current= node #walk up from the current node to the root
    while current is not None:
        current.visits += 1#increase visit count
        current.total_points+= reward#add simulation reward
        current= current.parent#move to parent

def mcts(state, iterations=1000):
    if state.is_terminal():#if state is terminal there is no move to make
        return None
    root= MCTSNode(state)
        
    root_player= state.current_player
    for _ in range(iterations):#runs MCTS for the amount of number of iterations
        node= root
        while not node.is_terminal() and node.fully_expanded():#seletions, keeps moving down while node is non terminal
                node = node.best_child()
        if not node.is_terminal() and not node.fully_expanded():#expansions
                node = node.expand()
        reward =simulate_random_play(node.state, root_player)#simulations play randomly from the new node until the game ends
        backpropagate(node, reward)#back propagation

    best_child = max(root.children, key=lambda child: child.visits)
    return best_child.move