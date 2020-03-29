from enum import Enum
import numpy as np
from disjoint_set import DisjoinSet
from random import choice


class Player(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2

class Border(Enum):
    ONE = 0
    TWO = 1

class State:
    def __init__(self, size):
        self.size = size
        self.board = np.int_(np.zeros((size, size)))
        self.player = Player.WHITE
        self.white_fields = DisjoinSet()
        self.black_fields = DisjoinSet()

    def get_moves(self):
        moves = []
        for x, y in np.ndindex((self.size, self.size)):
            if self.board[x, y] == Player.NONE.value:
                moves.append((x, y))
        return moves

    def make_move(self, cell):
        if self.board[cell] != Player.NONE.value:
            raise ValueError('This cell is already taken.')

        self.board[cell] = self.player.value
        if self.player == Player.WHITE:
            self._add_to_set(self.white_fields, 0, Player.WHITE, cell)
            self.player = Player.BLACK
        else:
            self._add_to_set(self.black_fields, 1, Player.BLACK, cell)
            self.player = Player.WHITE

    def _add_to_set(self, fields, component, player, cell):
        if cell[component] == 0:
            fields.union(Border.ONE.value, cell)
        elif cell[component] == self.size-1:
            fields.union(Border.TWO.value, cell)

        for n in self.get_neighbours(cell):
            if self.board[n] == player.value:
                fields.union(cell, n)

    def get_neighbours(self, cell):
        return [(cell[0] + n[0], cell[1] + n[1]) for n in ((-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, -1))
                if (0 <= cell[0] + n[0] < self.size and 0 <= cell[1] + n[1] < self.size)]

    def get_status(self):
        if self.white_fields.are_connected(Border.ONE.value, Border.TWO.value):
            return Player.WHITE
        if self.black_fields.are_connected(Border.ONE.value, Border.TWO.value):
            return Player.BLACK
        return Player.NONE

    def __str__ (self):
        cell_size = len(str(self.size))
        def represent(value):
            return str(value) + ' '*(cell_size - len(str(value)))

        white = represent('W')
        black = represent('B')
        empty = represent('.')
        offset = 1
        new_line = '\n'

        board_str = new_line + "Current player: {}".format(self.player) + new_line
        board_str += ' ' + ' ' * cell_size

        for i in range(self.size):
            board_str += represent(i) + ' ' * (offset * 2)
        board_str += new_line

        for y in range(self.size):
            board_str += ' '* offset * y + represent(y) + ' '*(offset*2)
            for x in range(self.size):
                if self.board[x, y] == Player.WHITE.value:
                    board_str += white
                elif self.board[x, y] == Player.BLACK.value:
                    board_str += black
                else:
                    board_str += empty
                board_str += ' ' * offset * 2
            board_str += white + new_line

        board_str += ' ' * (cell_size+offset) + ' ' * (offset * self.size + 1) + (black + ' ' * offset * 2) * self.size
        return board_str


def play(size):
    s = State(size=size)
    while True:
        if s.player == Player.BLACK:
            move = choice(s.get_moves())
            s.make_move(move)
        else:
            print(s)
            user_input = input('Enter move x,y: ')
            user_input = user_input.split(',')
            x = int(user_input[0])
            y = int(user_input[1])
            try:
                s.make_move((x, y))
            except (ValueError, IndexError) as e:
                print(e)
                continue

        status = s.get_status()
        if status == Player.WHITE:
            print("You win")
            break
        elif status == Player.BLACK:
            print("You lose")
            break

if __name__ == '__main__':
    play(size=5)