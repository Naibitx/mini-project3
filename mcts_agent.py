import math
import random
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

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c=1.41):
        best_score = float("-inf")
        best_node = None

        for child in self.children:
            if child.visits == 0:
                score = float("inf")
            else:
                exploitation = child.wins / child.visits
                exploration = c * math.sqrt(math.log(self.visits) / child.visits)
                score = exploitation + exploration

            if score > best_score:
                best_score = score
                best_node = child

        return best_node

    def best_move(self):
        if not self.children:
            return None
        return max(self.children, key=lambda child: child.visits).move


def select(node):
    while not node.state.is_terminal() and node.is_fully_expanded():
        node = node.best_child()
    return node


def expand(node):
    move = random.choice(node.untried_moves)
    node.untried_moves.remove(move)

    child_state = node.state.make_move(move)
    child_node = MCTSNode(child_state, parent=node, move=move)
    node.children.append(child_node)

    return child_node


def simulate(state):
    current_state = state

    while not current_state.is_terminal():
        move = random.choice(current_state.get_legal_moves())
        current_state = current_state.make_move(move)

    return current_state.utility()


def backpropagate(node, result):
    while node is not None:
        node.visits += 1

        if node.move is not None:
            player_who_moved = -node.state.current_player
            if result == player_who_moved:
                node.wins += 1

        node = node.parent


def mcts(state, iterations=1000):
    root = MCTSNode(state)

    for _ in range(iterations):
        leaf = select(root)

        if not leaf.state.is_terminal():
            leaf = expand(leaf)

        result = simulate(leaf.state)
        backpropagate(leaf, result)

    return root.best_move()


if __name__ == "__main__":
    state = TicTacToe()

    move = mcts(state, iterations=10000)
    print("MCTS move from empty board:", move)

    win_state = TicTacToe()
    win_state.board = [
        1, 1, 0,
        -1, -1, 0,
        0, 0, 0
    ]
    win_state.current_player = 1
    print("Winning move test:", mcts(win_state, iterations=500))

    block_state = TicTacToe()
    block_state.board = [
        -1, -1, 0,
         1,  0, 0,
         1,  0, 0
    ]
    block_state.current_player = 1
    print("Blocking move test:", mcts(block_state, iterations=500))