def minimax(state):
    # Return the best move for the current player.
    if state.current_player == 1:
        best_value = float('-inf')
        best_move = None
        for move in state.get_legal_moves():
            child = state.make_move(move)
            value = min_value(child)
            if value > best_value:
                best_value = value
                best_move = move
            return best_move
        else:
            # TODO: implement the symmetric case
            # for MIN.
            pass

def max_value(state):
    if state.is_terminal():
        return state.utility()
    v = float('-inf')
    for move in state.get_legal_moves():
        child = state.make_move(move)
        v = max(v, min_value(child))
        return v
    
def min_value(state):
    # TODO: implement. This is symmetric max_value, but minimizes instead. 
    pass