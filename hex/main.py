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
    t_start = time()
    player = 0
    while game.get_winner() == Player.NONE:
        if debug:
            print(game)

        move = players[player].get_move()
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

    return game.get_winner(), t_stop - t_start


if __name__ == '__main__':
    random.seed(0)
    N = 30
    for i in range(N):
        game = State(8)
        
        agents = [
            MCTSAgent(game, 10),
            NegamaxAgent(game, 2, shortest_connecting_path_length),
            #RandomAgent(game, random),
            #UserAgent(game)
        ]

        white_wins = 0
        winner, elapsed_time = play(game, agents, debug=True)

        if winner == Player.WHITE:
            white_wins += 1
        
        print('{}: {} (time: {})'.format(i, winner, elapsed_time))
    
    percentages_of_white_wins = round(white_wins/N*100,2)
    print('White player wins in {}% games'.format(percentages_of_white_wins))
