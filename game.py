class TicTacToe:
    def __init__(self):
        # 0 = empty, 1 = X, -1 = O
        self.board = [0] * 9
        self.current_player = 1

    def get_legal_moves(self):
        moves = []
        for i in range(9):
            if self.board[i] == 0:
                moves.append(i)
        return moves

    def make_move(self, move):
        if move not in self.get_legal_moves():
            raise ValueError("Invalid move")

        new_state = TicTacToe()
        new_state.board = self.board.copy()
        new_state.current_player = self.current_player

        new_state.board[move] = self.current_player
        new_state.current_player = -self.current_player

        return new_state

    def is_terminal(self):
        if self.check_winner() != 0:
            return True
        if len(self.get_legal_moves()) == 0:
            return True
        return False

    def utility(self):
        if not self.is_terminal():
            raise ValueError("Utility is only valid for terminal states")

        winner = self.check_winner()

        if winner == 1:
            return 1
        elif winner == -1:
            return -1
        else:
            return 0

    def check_winner(self):
        winning_lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6)
        ]

        for a, b, c in winning_lines:
            if self.board[a] != 0 and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]

        return 0

    def display(self):
        symbols = {1: "X", -1: "O", 0: "."}

        for i in range(0, 9, 3):
            row = self.board[i:i+3]
            print(" ".join(symbols[cell] for cell in row))

