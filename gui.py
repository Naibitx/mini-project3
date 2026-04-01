import tkinter as tk
from tkinter import ttk
import random

from game import TicTacToe
from minimax_agent import minimax
from mcts_agent import mcts


def random_agent(state):
    return random.choice(state.get_legal_moves())


def mcts_agent_1000(state):
    return mcts(state, iterations=1000)


class TicTacToeGUI:
    def __init__(self):
        self.state = TicTacToe()
        self.running = False
        self.delay = 800

        self.agent_map = {
            "Random": random_agent,
            "Minimax": minimax,
            "MCTS (1000)": mcts_agent_1000
        }

        self.cell_size = 100
        self.padding = 20
        self.size = self.cell_size * 3 + self.padding * 2

        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe Agent Viewer")

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10)

        tk.Label(self.top_frame, text="X Agent:").grid(row=0, column=0, padx=5)
        self.x_agent_var = tk.StringVar(value="Minimax")
        self.x_menu = ttk.Combobox(
            self.top_frame,
            textvariable=self.x_agent_var,
            values=list(self.agent_map.keys()),
            state="readonly",
            width=12
        )
        self.x_menu.grid(row=0, column=1, padx=5)

        tk.Label(self.top_frame, text="O Agent:").grid(row=0, column=2, padx=5)
        self.o_agent_var = tk.StringVar(value="MCTS (1000)")
        self.o_menu = ttk.Combobox(
            self.top_frame,
            textvariable=self.o_agent_var,
            values=list(self.agent_map.keys()),
            state="readonly",
            width=12
        )
        self.o_menu.grid(row=0, column=3, padx=5)

        tk.Label(self.top_frame, text="Delay (ms):").grid(row=0, column=4, padx=5)
        self.delay_var = tk.StringVar(value="800")
        self.delay_entry = tk.Entry(self.top_frame, textvariable=self.delay_var, width=8)
        self.delay_entry.grid(row=0, column=5, padx=5)

        self.start_button = tk.Button(self.root, text="Start Match", command=self.start_match)
        self.start_button.pack(pady=5)

        self.reset_button = tk.Button(self.root, text="Reset Board", command=self.reset_board)
        self.reset_button.pack(pady=5)

        self.status_label = tk.Label(self.root, text="Choose agents and start a match.", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=self.size, height=self.size, bg="#69c3b0")
        self.canvas.pack(padx=10, pady=10)

        self.redraw()

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

    def redraw(self):
        self.canvas.delete("all")
        self.draw_board()
        self.draw_marks()
        self.root.update_idletasks()

    def reset_board(self):
        if self.running:
            return
        self.state = TicTacToe()
        self.status_label.config(text="Board reset. Choose agents and start a match.")
        self.redraw()

    def get_current_agent(self):
        if self.state.current_player == 1:
            return self.agent_map[self.x_agent_var.get()], "X"
        else:
            return self.agent_map[self.o_agent_var.get()], "O"

    def start_match(self):
        if self.running:
            return

        try:
            self.delay = int(self.delay_var.get())
        except ValueError:
            self.delay = 800
            self.delay_var.set("800")

        self.state = TicTacToe()
        self.running = True
        self.start_button.config(state="disabled")
        self.status_label.config(
            text=f"Starting: X = {self.x_agent_var.get()} vs O = {self.o_agent_var.get()}"
        )
        self.redraw()
        self.root.after(self.delay, self.step_match)

    def step_match(self):
        if self.state.is_terminal():
            winner = self.state.check_winner()

            if winner == 1:
                self.status_label.config(text="Game Over: X wins")
            elif winner == -1:
                self.status_label.config(text="Game Over: O wins")
            else:
                self.status_label.config(text="Game Over: Draw")

            self.running = False
            self.start_button.config(state="normal")
            return

        agent_func, player_name = self.get_current_agent()
        move = agent_func(self.state)

        self.status_label.config(text=f"{player_name} chooses square {move}")
        self.state = self.state.make_move(move)
        self.redraw()

        self.root.after(self.delay, self.step_match)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TicTacToeGUI()
    app.run()