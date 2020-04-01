from hex.agents.base_agent import BaseAgent
from collections import defaultdict
import numpy as np
from copy import deepcopy


class NegamaxAgent(BaseAgent):
    def __init__(self, game, depth, heuristic):
        self.game = game
        self.depth = depth
        self.heuristic = heuristic
        self.transposition_table = defaultdict(lambda x: None)

    def get_move(self):
        # alpha-beta tba.
        return self.best_evaluated_move(self.game, self.depth)[0]

    def register_move(self, move):
        pass

    def best_evaluated_move(self, game, depth):
        best_move = None
        max_heuristic = -np.inf
        for move in self.game.get_moves():

            current_game = deepcopy(game)
            current_game.make_move(move)
            current_heuristic = self.transposition_table[
                (current_game, depth)]  # should work as both components of tuple are immutable

            if current_heuristic is None:
                if depth == 0:
                    current_heuristic = self.heuristic(current_game)
                else:
                    current_heuristic = - \
                        self.best_evaluated_move(current_game, depth-1)[1]
                self.transposition_table[(
                    current_game, depth)] = current_heuristic

            if current_heuristic > max_heuristic:
                best_move = move
                max_heuristic = current_heuristic

        return (best_move, max_heuristic)
