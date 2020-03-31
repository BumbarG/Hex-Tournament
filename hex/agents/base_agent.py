class BaseAgent:
    def get_move(self):
        raise NotImplementedError()

    def register_move(self, move):
        raise NotImplementedError()
