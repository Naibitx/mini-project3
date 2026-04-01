import tkinter as tk
from game import TicTacToe


class TicTacToeGUI:
    def __init__(self, state):
        self.state = state
        self.cell_size = 100
        self.padding = 20
        self.size = self.cell_size * 3 + self.padding * 2

        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")

        self.canvas = tk.Canvas(
            self.root,
            width=self.size,
            height=self.size,
            bg="#69c3b0"
        )
        self.canvas.pack()

        self.draw_board()
        self.draw_marks()

    def draw_board(self):
        for i in range(1, 3):
            x = self.padding + i * self.cell_size
            y = self.padding + i * self.cell_size

            self.canvas.create_line(
                x, self.padding, x, self.size - self.padding,
                width=4, fill="#4f6b6b"
            )
            self.canvas.create_line(
                self.padding, y, self.size - self.padding, y,
                width=4, fill="#4f6b6b"
            )

    def draw_marks(self):
        for i in range(9):
            row = i // 3
            col = i % 3

            x1 = self.padding + col * self.cell_size + 20
            y1 = self.padding + row * self.cell_size + 20
            x2 = self.padding + (col + 1) * self.cell_size - 20
            y2 = self.padding + (row + 1) * self.cell_size - 20

            if self.state.board[i] == 1:
                self.canvas.create_line(x1, y1, x2, y2, width=5, fill="#4f4f4f")
                self.canvas.create_line(x1, y2, x2, y1, width=5, fill="#4f4f4f")

            elif self.state.board[i] == -1:
                self.canvas.create_oval(x1, y1, x2, y2, width=5, outline="#f3eed9")

    def show(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.board = [
        0, -1, 1,
        1,  1, -1,
        -1, 1, -1
    ]

    gui = TicTacToeGUI(game)
    gui.show()