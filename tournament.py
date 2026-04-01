import random
from game import TicTacToe
from minimax_agent import minimax
from mcts_agent import mcts


def random_agent(state):
    return random.choice(state.get_legal_moves())


def mcts_agent_1000(state):
    return mcts(state, iterations=1000)


def play_game(agent_x, agent_o, show_board=False):
    state = TicTacToe()

    if show_board:
        print("New game")
        state.display()
        print()

    while not state.is_terminal():
        if state.current_player == 1:
            move = agent_x(state)
        else:
            move = agent_o(state)

        state = state.make_move(move)

        if show_board:
            state.display()
            print()

    winner = state.check_winner()

    if winner == 1:
        return "X"
    elif winner == -1:
        return "O"
    else:
        return "Draw"


def run_matchup(agent_x, agent_o, num_games=100, show_first_game=False):
    results = {"X": 0, "O": 0, "Draw": 0}

    for i in range(num_games):
        show_board = show_first_game and i == 0
        result = play_game(agent_x, agent_o, show_board=show_board)
        results[result] += 1

    return results


def print_results_table(results_dict):
    print("\nTournament Results")
    print("-" * 72)
    print(f"{'Matchup':35} {'X Wins':>10} {'O Wins':>10} {'Draws':>10}")
    print("-" * 72)

    for matchup, results in results_dict.items():
        print(
            f"{matchup:35} "
            f"{results['X']:>10} "
            f"{results['O']:>10} "
            f"{results['Draw']:>10}"
        )

    print("-" * 72)


def main():
    all_results = {}

    all_results["Minimax (X) vs Random (O)"] = run_matchup(
        minimax,
        random_agent,
        num_games=100
    )

    all_results["MCTS 1000 (X) vs Random (O)"] = run_matchup(
        mcts_agent_1000,
        random_agent,
        num_games=100
    )

    all_results["Minimax (X) vs MCTS 1000 (O)"] = run_matchup(
        minimax,
        mcts_agent_1000,
        num_games=100
    )

    all_results["MCTS 1000 (X) vs Minimax (O)"] = run_matchup(
        mcts_agent_1000,
        minimax,
        num_games=100
    )

    print_results_table(all_results)


if __name__ == "__main__":
    main()