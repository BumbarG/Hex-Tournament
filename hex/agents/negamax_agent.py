from collections import defaultdict
from copy import deepcopy

import numpy as np

from agents.base_agent import BaseAgent
from system.enums import Player

class NegamaxAgent(BaseAgent):
    def __init__(self, game, depth, heuristic):
        self.game = game
        self.depth = depth
        self.heuristic = heuristic

    def get_move(self):
        # alpha-beta tba.
        move, score = self.best_evaluated_move(self.game, self.depth, -np.inf, np.inf)
        return move

    def register_move(self, move):
        pass

    def best_evaluated_move(self, game, depth, alpha, beta):
        if depth == 0 or game.get_winner() != Player.NONE:
            #print(game)
            score = self.heuristic(game)
            #print(score)
            return None, score

        best_move = None
        max_heuristic = -np.inf
        for move in game.get_moves():
            current_game = deepcopy(game)
            current_game.make_move(move)

            current_heuristic = - self.best_evaluated_move(current_game, depth-1, -beta, -alpha)[1]
            if current_heuristic > max_heuristic:
                best_move = move
                max_heuristic = current_heuristic

                # only if current_heuristic is greater than max_heuristic, the alpha may change
                alpha = max(alpha, max_heuristic)
                if alpha >= beta:
                    break

        return (best_move, max_heuristic)
