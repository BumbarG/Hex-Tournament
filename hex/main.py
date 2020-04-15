from agents.mcts_agent import MCTSAgent
from agents.random_agent import RandomAgent
from agents.negamax_agent import NegamaxAgent
from agents.user_agent import UserAgent
from system.enums import Player
from system.state import State
from libs.heuristics import shortest_connecting_path_length


def play(game, players, debug=False):
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

    print("Winner is player {}".format(game.get_winner()))


if __name__ == '__main__':
    game = State(8)

    # agent1 = MCTSAgent(game, 30)
    agent1 = NegamaxAgent(game, 2, shortest_connecting_path_length)
    #agent1 = RandomAgent(game)
    agent2 = UserAgent(game)

    play(game, [agent1, agent2], debug=True)
