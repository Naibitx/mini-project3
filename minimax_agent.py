def minimax_ab(state):
    alpha = float('-int')
    beta = float('inf')
    # Return the best move for the current player.
    if state.current_player == 1: # max player
        best_value = float('-inf')
        best_move = None
        for move in state.get_legal_moves():
            child = state.make_move(move)
            value = min_value_ab(child, alpha, beta)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
        return best_move
    else: # MIN player
        # TODO: implement the symmetric case
        best_value = float('inf')
        best_move = None
        for move in state.get_legal_moves():
            child = state.make_move(move)
            value = max_value_ab(child, alpha, beta)
            if value < best_value:
                best_value = value
                best_move = move
            beta =  min(beta, best_value)
        return best_move

def max_value_ab(state, alpha, beta):
    if state.is_terminal():
        return state.utility()
    v = float('-inf')
    for move in state.get_legal_moves():
        child = state.make_move(move)
        v = max(v, min_value_ab(child, alpha, beta))
        if v >= beta:
            return v # Beta
        alpha = max(alpha, v)
    return v
    
def min_value_ab(state, alpha, beta):
    # TODO: implement. This is symmetric max_value, but minimizes instead. 
    if state.is_terminal():
        return state.utility()
    v = float('inf')
    for move in state.get_legal_moves():
        child = state.make_move(move)
        v = min(v, max_value_ab(child, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v