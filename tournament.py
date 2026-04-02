import random
import time
import matplotlib.pyplot as plt

from game import TicTacToe
from minimax_agent import minimax_ab
from mcts_agent import mcts

def rand_agent(state):
    return random.choice(state.get_legal_moves())
def make_mcts_agent(iterations):
    def agent(state):
        return mcts(state, iterations=iterations)
    return agent

def play_game(x_agent, o_agent):
    state = TicTacToe()

    x_total_time= 0.0
    o_total_time= 0.0
    x_moves= 0
    o_moves= 0

    while not state.is_terminal():
        if state.current_player== 1:
            start= time.perf_counter()
            move= x_agent(state)
            end= time.perf_counter()

            x_total_time+= (end - start)
            x_moves+= 1
        else:
            start= time.perf_counter()
            move= o_agent(state)
            end= time.perf_counter()

            o_total_time += (end - start)
            o_moves += 1
        state= state.make_move(move)
    winner= state.check_winner()

    if winner== 1:
        result= "X"
    elif winner== -1:
        result= "O"
    else:
        result= "Draw"
    x_avg_time= x_total_time / x_moves if x_moves > 0 else 0.0
    o_avg_time= o_total_time / o_moves if o_moves > 0 else 0.0
    return result, x_avg_time, o_avg_time

def run_matchup(name, x_agent, o_agent, num_games=100):
    x_wins= 0
    o_wins= 0
    draws= 0

    total_x_avg= 0.0
    total_o_avg= 0.0

    for _ in range(num_games):
        result, x_avg_time, o_avg_time = play_game(x_agent, o_agent)
        if result== "X":
            x_wins+= 1
        elif result== "O":
            o_wins+= 1
        else:
            draws+= 1
        total_x_avg += x_avg_time
        total_o_avg += o_avg_time

    avg_x_time= total_x_avg / num_games
    avg_o_time= total_o_avg / num_games

    return {
        "matchup": name,
        "games": num_games,
        "x_wins": x_wins,
        "o_wins": o_wins,
        "draws": draws,
        "x_avg_time": avg_x_time,
        "o_avg_time": avg_o_time
    }
def print_results_table(results):
    print("\nTOURNAMENT RESULTS")
    print("-" * 95)
    print(
        f"{'Matchup':35} {'Games':>6} {'X Wins':>8} {'O Wins':>8} {'Draws':>8} "
        f"{'X Avg Time':>14} {'O Avg Time':>14}"
    )
    print("-" * 95)
    for r in results:
        print(
            f"{r['matchup']:35} "
            f"{r['games']:>6} "
            f"{r['x_wins']:>8} "
            f"{r['o_wins']:>8} "
            f"{r['draws']:>8} "
            f"{r['x_avg_time']:>14.6f} "
            f"{r['o_avg_time']:>14.6f}"
        )
    print("-" * 95)
def measure_mcts_timing(iteration_counts, games_per_setting=20):
    times = []

    for iterations in iteration_counts:
        mcts_agent = make_mcts_agent(iterations)
        total_avg_time = 0.0

        for _ in range(games_per_setting):
            _, x_avg_time, _ = play_game(mcts_agent, rand_agent)
            total_avg_time += x_avg_time

        overall_avg = total_avg_time / games_per_setting
        times.append(overall_avg)

    return times

def plot_mcts_timing(iteration_counts, times, filename="mcts_timing_graph.png"):
    plt.figure(figsize=(8, 5))
    plt.plot(iteration_counts, times, marker="o")
    plt.xlabel("MCTS Iterations")
    plt.ylabel("Average Time per Move (seconds)")
    plt.title("MCTS Iterations vs Average Time per Move")
    plt.grid(True)
    plt.savefig(filename, bbox_inches="tight")
    plt.show()


def main():
    num_games= 5
    mcts_1000= make_mcts_agent(1000)
    results= []
    results.append(
        run_matchup("Minimax (X) vs Random (O)", minimax_ab, rand_agent, num_games)
    )
    results.append(
        run_matchup("MCTS-1000 (X) vs Random (O)", mcts_1000, rand_agent, num_games)
    )
    results.append(
        run_matchup("Minimax (X) vs MCTS-1000 (O)", minimax_ab, mcts_1000, num_games)
    )
    results.append(
        run_matchup("MCTS-1000 (X) vs Minimax (O)", mcts_1000, minimax_ab, num_games)
    )
    print_results_table(results)

    iteration_counts = [100, 500, 1000, 5000, 10000]
    mcts_times = measure_mcts_timing(iteration_counts, games_per_setting=20)

    print("\nMCTS TIMING RESULTS")
    print("-" * 45)
    print(f"{'Iterations':>12} {'Avg Time per Move (s)':>25}")
    print("-" * 45)
    for iterations, avg_time in zip(iteration_counts, mcts_times):
        print(f"{iterations:>12} {avg_time:>25.6f}")
    print("-" * 45)

    minimax_total = 0.0
    minimax_games = 20
    for _ in range(minimax_games):
        _, x_avg_time, _= play_game(minimax_ab, rand_agent)
        minimax_total+= x_avg_time
    minimax_avg= minimax_total / minimax_games
    print(f"\nMinimax average time per move: {minimax_avg:.6f} seconds")
    plot_mcts_timing(iteration_counts, mcts_times)

if __name__== "__main__":
    main()