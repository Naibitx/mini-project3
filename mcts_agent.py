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

    def terminal(self):
        return self.state.terminal()#true if node state is terminal
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