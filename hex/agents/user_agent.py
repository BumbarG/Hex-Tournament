from hex.agents.base_agent import BaseAgent


class UserAgent(BaseAgent):
    def get_move(self):
        user_input = input('Enter move x,y: ').split(',')
        return (int(user_input[0]), int(user_input[1]))

    def register_move(self, move):
        pass
