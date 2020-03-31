from random import choice

from hex.agents.base_agent import BaseAgent


class RandomAgent(BaseAgent):
    def __init__(self, game):
        self.game = game

    def get_move(self):
        moves = self.game.get_moves()
        return choice(moves)

    def register_move(self, move):
        pass
