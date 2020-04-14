from copy import deepcopy
from math import log, sqrt
from random import choice, shuffle
from time import time

from agents.base_agent import BaseAgent
from system.enums import Player


class Node:
    def __init__(self, explore_factor, parent=None, move=None):
        self.N = 0
        self.Q = 0
        self.parent = parent
        self.children = {}
        self.move = move
        self.explore_factor = explore_factor

    def get_value(self):
        if self.N == 0:
            return float('inf')
        else:
            return self.Q / self.N + self.explore_factor * sqrt(2 * log(self.parent.N) / self.N)


class MCTS:
    def __init__(self, game, search_seconds, explore_factor):
        self.game = game
        self.search_seconds = search_seconds
        self.explore_factor = explore_factor
        self.root = Node(self.explore_factor)

    def search(self):
        """
        Execute Monte Carlo Tree evaluation for search_seconds time
        """
        t_start = time()
        while time() - t_start < self.search_seconds:
            state, urgent_node = self.__select_urgent_node()
            selected_node = self.__expand_and_select(state, urgent_node)
            current_player = state.player
            winner = self.__rollout(state)
            self.__backup(selected_node, current_player, winner)

    def get_best_move(self):
        max_value = max([n.get_value() for _, n in self.root.children.items()])
        node = choice([n for _, n in self.root.children.items()
                       if n.get_value() == max_value])
        return node.move

    def make_move(self, move):
        # game state is updated directly by reference
        if move not in self.root.children:
            self.root = Node(self.explore_factor)
        else:
            self.root = self.root.children[move]
            self.root.parent = None

    def __select_urgent_node(self):
        """
        Select the node that we are going to expand
        """
        state = deepcopy(self.game)
        node = self.root

        while len(node.children) > 0 and node.N > 0:
            max_value = max([n.get_value() for _, n in node.children.items()])
            node = choice([n for _, n in node.children.items()
                           if n.get_value() == max_value])
            state.make_move(node.move)

        return state, node

    def __expand_and_select(self, state, urgent_node):
        if state.get_winner() != Player.NONE:
            return urgent_node  # this is terminal node

        for move in state.get_moves():
            urgent_node.children[move] = Node(
                self.explore_factor, urgent_node, move)

        move, selected_node = choice(list(urgent_node.children.items()))
        state.make_move(selected_node.move)
        return selected_node

    def __rollout(self, state):
        moves = state.get_moves()
        shuffle(moves)
        for move in moves:
            state.make_move(move)

        return state.get_winner()

    def __backup(self, node, current_player, winner):
        # profit is for previos player, not current
        profit = not (current_player == winner)
        while node is not None:
            node.N += 1
            node.Q += int(profit)
            profit = not profit
            node = node.parent


class MCTSAgent(BaseAgent):
    def __init__(self, game, search_seconds, explore_factor=0.5):
        self.mcts = MCTS(game, search_seconds, explore_factor)

    def get_move(self):
        self.mcts.search()
        return self.mcts.get_best_move()

    def register_move(self, move):
        self.mcts.make_move(move)
