from hex.agents.base_agent import BaseAgent
from system.enums import Player
from collections import defaultdict
import numpy as np


class negamaxAgent(BaseAgent):
    def __init__(self, game, depth, heuristic):
        self.game = game
        self.depth = depth
        self.heuristic = heuristic
        self.transposition_table = defaultdict(lambda x: None)

    def get_move(self):
        # alpha-beta tba.
        return self.best_evaluated_move(self.depth)[0]

    def register_move(self, move):
        pass

    def best_evaluated_move(self, depth):
        if depth == 0:
            best_move = None
            max_heuristic = -np.inf
            for move in self.game.get_moves():
                self.game.make_move(move)
                current_heuristic = self.transposition_table(
                    (self.game, depth))

                if current_heuristic is None:
                    if depth == 0:
                        current_heuristic = self.heuristic(self.game)
                    else:
                        current_heuristic = - \
                            self.best_evaluated_move(depth-1)[1]
                    self.transposition_table[(
                        self.game, depth)] = current_heuristic

                if current_heuristic > max_heuristic:
                    best_move = move
                    max_heuristic = current_heuristic
                self.game.undo_move(move)  # needs to be implemented

        return (best_move, max_heuristic)
