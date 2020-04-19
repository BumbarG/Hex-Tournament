from agents.base_agent import BaseAgent


class RandomAgent(BaseAgent):
    def __init__(self, game, rnd):
        self.game = game
        self.rnd = rnd

    def get_move(self):
        moves = self.game.get_moves()
        return self.rnd.choice(moves)

    def register_move(self, move):
        pass
