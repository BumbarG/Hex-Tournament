import random
from time import time

from agents.mcts_agent import MCTSAgent
from agents.negamax_agent import NegamaxAgent
from agents.random_agent import RandomAgent
from agents.user_agent import UserAgent
from libs.heuristics import shortest_connecting_path_length
from system.enums import Player
from system.state import State


def play(game, players, debug=False):
    number_of_moves = [0, 0] # for each player
    time_for_all_moves = [0, 0] # for each player :)
    t_start = time()
    player = 0
    while game.get_winner() == Player.NONE:
        number_of_moves[player] += 1
        if debug:
            print(game)
        t_move_start = time()
        move = players[player].get_move()
        t_move_stop = time()
        time_for_all_moves[player] += t_move_stop - t_move_start
        if debug:
            print("Selected move: {}".format(move))
        game.make_move(move)

        for p in players:
            p.register_move(move)

        player = (player + 1) % 2

    t_stop = time()
    if debug:
        print("Winner is player {}".format(game.get_winner()))
        print(game)

    return game.get_winner(), t_stop - t_start, number_of_moves, time_for_all_moves


if __name__ == '__main__':
    random.seed(0)

    N = 5
    game_size = 8

    agents = [
        #agent engine, (arguments after game)
        (RandomAgent, (random,)),
        (MCTSAgent, (4,)),
        (NegamaxAgent, (2, shortest_connecting_path_length))
    ]

    for i in range(len(agents)):
        for j in range(len(agents)):
            # Player i vs. Player j
            print("-----------------------------")
            print("Player {} vs. Player {}".format(i, j))
            print("-----------------------------")

            player1_engine = agents[i][0]
            player1_args = agents[i][1]
            
            player2_engine = agents[j][0]
            player2_args = agents[j][1]

            total_games = 0
            white_wins = 0
            all_moves = [0, 0]
            all_time = [0, 0]

            for k in range(N):
                game = State(game_size)

                current_agents = [
                    player1_engine(game, *player1_args),
                    player2_engine(game, *player2_args)
                ]

                winner, elapsed_time, number_of_moves, time_for_all_moves = play(game, current_agents, debug=False)

                avg_time_per_move1 = time_for_all_moves[0] / number_of_moves[0]
                avg_time_per_move2 = time_for_all_moves[1] / number_of_moves[1]

                all_moves[0] += number_of_moves[0]
                all_moves[1] += number_of_moves[1]

                all_time[0] += time_for_all_moves[0]
                all_time[1] += time_for_all_moves[1]

                print("Winner is {} (ttime: {}, tmoves: {}, time per move: [{}, {}])".format(
                    winner, 
                    elapsed_time, 
                    number_of_moves[0] + number_of_moves[1],
                    avg_time_per_move1,
                    avg_time_per_move2
                    ))

                total_games += 1
                if winner == Player.WHITE:
                    white_wins += 1

            percentages_of_white_wins = round(white_wins/N*100,2)
            avg_time_per_move1 = all_time[0] / all_moves[0]
            avg_time_per_move2 = all_time[1] / all_moves[1]
            avg_number_of_moves_per_game = (all_moves[0] + all_moves[1])/ total_games

            print('White wins in {}% games (avg number of moves per game: {}, avg time for one move: [{}, {}]'.format(
                avg_number_of_moves_per_game,
                percentages_of_white_wins,
                avg_time_per_move1,
                avg_time_per_move2
                ))
