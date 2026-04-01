from game import TicTacToe

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.get_legal_moves()

def select(node):
    pass

def expand(node):
    pass

def simulate(state):
    pass

def backpropagate(node, result):
    pass

def mcts(state, iterations=1000):
    pass