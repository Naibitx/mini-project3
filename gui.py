import tkinter as tk
from tkinter import ttk, messagebox
import random

from game import TicTacToe
from minimax_agent import minimax_ab
from mcts_agent import mcts

def random_agent(state):
    return random.choice(state.get_legal_moves())


def mcts_agent_1000(state):
    return mcts(state, iterations=1000)

#all to count the nodes
plain_nodes= 0
ab_nodes= 0


def minimax_plain(state):
    global plain_nodes
    if state.current_player== 1:
        best_value = float('-inf')
        best_move = None
        for move in state.get_legal_moves():
            child = state.make_move(move)
            value = min_value_plain(child)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move
    else:
        best_value= float('inf')
        best_move= None
        for move in state.get_legal_moves():
            child= state.make_move(move)
            value= max_value_plain(child)
            if value< best_value:
                best_value= value
                best_move= move
        return best_move


def max_value_plain(state):
    global plain_nodes
    plain_nodes+= 1

    if state.is_terminal():
        return state.utility()

    v= float('-inf')
    for move in state.get_legal_moves():
        child= state.make_move(move)
        v= max(v, min_value_plain(child))
    return v
def min_value_plain(state):
    global plain_nodes
    plain_nodes += 1

    if state.is_terminal():
        return state.utility()

    v= float('inf')
    for move in state.get_legal_moves():
        child= state.make_move(move)
        v= min(v, max_value_plain(child))
    return v


def minimax_ab_counted(state):
    global ab_nodes
    alpha= float('-inf')
    beta= float('inf')

    if state.current_player== 1:
        best_value= float('-inf')
        best_move= None
        for move in state.get_legal_moves():
            child= state.make_move(move)
            value= min_value_ab(child, alpha, beta)
            if value> best_value:
                best_value= value
                best_move= move
            alpha= max(alpha, best_value)
        return best_move
    else:
        best_value= float('inf')
        best_move= None
        for move in state.get_legal_moves():
            child= state.make_move(move)
            value= max_value_ab(child, alpha, beta)
            if value< best_value:
                best_value= value
                best_move= move
            beta= min(beta, best_value)
        return best_move
def max_value_ab(state, alpha, beta):
    global ab_nodes
    ab_nodes+= 1

    if state.is_terminal():
        return state.utility()

    v= float('-inf')
    for move in state.get_legal_moves():
        child= state.make_move(move)
        v= max(v, min_value_ab(child, alpha, beta))
        if v>= beta:
            return v
        alpha= max(alpha, v)
    return v
def min_value_ab(state, alpha, beta):
    global ab_nodes
    ab_nodes+= 1

    if state.is_terminal():
        return state.utility()

    v= float('inf')
    for move in state.get_legal_moves():
        child= state.make_move(move)
        v= min(v, max_value_ab(child, alpha, beta))
        if v<= alpha:
            return v
        beta= min(beta, v)
    return v
class TicTacToeGUI:
    def __init__(self):
        self.state = TicTacToe()
        self.running = False
        self.delay = 800

        self.agent_map = {
            "Random": random_agent,
            "Minimax": minimax_ab,
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

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(anchor="w", padx=20, pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(anchor="w", padx=20, pady=10)

        self.start_button = tk.Button(
            self.button_frame,
            text="Start Match",
            command=self.start_match,
            width=16
        )
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.tournament_button = tk.Button(
            self.button_frame,
            text="Tournament Mode",
            command=self.start_visual_tournament,
            width=16
        )
        self.tournament_button.grid(row=0, column=1, padx=5, pady=5)

        self.node_button = tk.Button(
            self.button_frame,
            text="Show Nodes",
            command=self.show_node_counts,
            width=16
        )
        self.node_button.grid(row=0, column=2, padx=5, pady=5)

        self.reset_button = tk.Button(
            self.button_frame,
            text="Reset Board",
            command=self.reset_board,
            width=16
        )
        self.reset_button.grid(row=0, column=3, padx=5, pady=5)

        self.status_label = tk.Label(
            self.root,
            text="Choose agents and start a match.",
            font=("Arial", 18)
        )
        self.status_label.pack(pady=10)

        self.score_label= tk.Label(
            self.root,
            text= "This are the tournament scores",
            font= ("Arial", 18)
        )
        self.score_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=self.size, height=self.size, bg="#69c3b0")
        self.canvas.pack(padx=10, pady=10)

        #all for the tournament
        self.visual_tournament_mode= False
        self.tournament_matchups= []
        self.current_matchup_index= 0
        self.games_per_matchup= 2
        self.current_game_number= 0
        self.matchup_scores= {"X": 0, "O": 0, "Draw": 0}

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
        self.visual_tournament_mode= False

        try:
            self.delay = int(self.delay_var.get())
        except ValueError:
            self.delay = 800
            self.delay_var.set("800")

        self.state = TicTacToe()
        self.running = True
        self.start_button.config(state="disabled")
        self.tournament_button.config(state="disabled")
        self.status_label.config(
            text=f"Starting: X = {self.x_agent_var.get()} vs O = {self.o_agent_var.get()}"
        )
        self.redraw()
        self.root.after(self.delay, self.step_match)

    def start_visual_tournament(self):
        if self.running:
            return
        try:
            self.delay= int(self.delay_var.get())
        except ValueError:
            self.delay= 800
            self.delay_var.set("800")
        self.visual_tournament_mode= True
        self.tournament_matchups= [
            ("Minimax", "Random"),
            ("MCTS (1000)", "Random"),
            ("Minimax", "MCTS (1000)"),
            ("MCTS (1000)", "Minimax")
        ]
        self.current_matchup_index= 0
        self.current_game_number= 1
        self.matchup_scores= {"X": 0, "O": 0, "Draw": 0}
        self.start_button.config(state="disabled")
        self.tournament_button.config(state="disabled")
        self.begin_current_tournament_game()

    def begin_current_tournament_game(self):
        if self.current_matchup_index>= len(self.tournament_matchups):
            self.running= False
            self.start_button.config(state="normal")
            self.tournament_button.config(state="normal")
            self.status_label.config(text="Visual tournament finished.")
            self.score_label.config(text="Tournament complete.")
            return

        x_name, o_name= self.tournament_matchups[self.current_matchup_index]
        self.x_agent_var.set(x_name)
        self.o_agent_var.set(o_name)

        self.state= TicTacToe()
        self.running= True
        self.status_label.config(
            text=(
                f"Matchup {self.current_matchup_index + 1}/4: "
                f"X = {x_name} vs O = {o_name} | "
                f"Game {self.current_game_number}/{self.games_per_matchup}"
            )
        )

        self.score_label.config(
            text=(
                f"Current matchup score — "
                f"X wins: {self.matchup_scores['X']} | "
                f"O wins: {self.matchup_scores['O']} | "
                f"Draws: {self.matchup_scores['Draw']}"
            )
        )

        self.redraw()
        self.root.after(self.delay, self.step_match)

    def finish_tournament_game(self, winner_text):
        if winner_text== "X":
            self.matchup_scores["X"]+= 1
        elif winner_text== "O":
            self.matchup_scores["O"]+= 1
        else:
            self.matchup_scores["Draw"]+= 1
        self.score_label.config(
            text=(
                f"Current matchup score — "
                f"X wins: {self.matchup_scores['X']} | "
                f"O wins: {self.matchup_scores['O']} | "
                f"Draws: {self.matchup_scores['Draw']}"
            )
        )
        if self.current_game_number< self.games_per_matchup:
            self.current_game_number+= 1
        else: 
            self.current_matchup_index+= 1
            self.current_game_number= 1
            self.matchup_scores= {"X": 0, "O": 0, "Draw": 0}
        self.root.after(1200, self.begin_current_tournament_game)

    def step_match(self):
        if self.state.is_terminal():
            winner = self.state.check_winner()
            if winner == 1:
                result_text = "X"
                self.status_label.config(text="Game Over: X wins")
            elif winner == -1:
                result_text = "O"
                self.status_label.config(text="Game Over: O wins")
            else:
                result_text = "Draw"
                self.status_label.config(text="Game Over: Draw")
            self.running = False
            if self.visual_tournament_mode:
                self.finish_tournament_game(result_text)
            else:
                self.start_button.config(state="normal")
                self.tournament_button.config(state="normal")
            return
        agent_func, player_name = self.get_current_agent()
        move = agent_func(self.state)
        self.status_label.config(text=f"{player_name} chooses square {move}")
        self.state = self.state.make_move(move)
        self.redraw()
        self.root.after(self.delay, self.step_match)

    def show_node_counts(self):
        global plain_nodes, ab_nodes
        state = TicTacToe()
        plain_nodes = 0
        plain_move = minimax_plain(state)
        ab_nodes = 0
        ab_move = minimax_ab_counted(state)
        pruned = ((plain_nodes - ab_nodes) / plain_nodes) * 100
        result_text = (
            f"Plain Minimax Move: {plain_move}\n"
            f"Plain Minimax Nodes: {plain_nodes}\n\n"
            f"Alpha-Beta Move: {ab_move}\n"
            f"Alpha-Beta Nodes: {ab_nodes}\n\n"
            f"Pruned: {pruned:.2f}%"
        )
        messagebox.showinfo("Node Count Results", result_text)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TicTacToeGUI()
    app.run()