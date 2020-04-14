from agents.base_agent import BaseAgent


class UserAgent(BaseAgent):
    def __init__(self, game):
        self.game = game

    def get_move(self):
        while True:
            user_input = input('Enter move x,y: ').split(',')
            try:
                move = (int(user_input[0]), int(user_input[1]))
                if move in self.game.get_moves():
                    return move
            except:
                pass

    def register_move(self, move):
        pass
