from copy import deepcopy

import numpy as np

from agents.base_agent import BaseAgent
from system.enums import Player
#from system.enums import TTFlag


class TranspositionEntry:
    def __init__(self, value, depth, flag):
        self.value = value
        self.depth = depth
        self.flag = flag


class NegamaxAgent(BaseAgent):
    def __init__(self, game, depth, heuristic):
        self.game = game
        self.depth = depth
        self.heuristic = heuristic
        #self.transposition_table = {} # Not used due to too low search depth

    def get_move(self):
        winning_move = self.get_winning_move()
        if winning_move is not None:
            return winning_move
        
        move, _ = self.best_evaluated_move(self.game, self.depth, -np.inf, np.inf)
        return move

    def register_move(self, move):
        pass

    def get_winning_move(self):
        for move in self.game.get_moves():
            current_game = deepcopy(self.game)
            current_game.make_move(move)
            if current_game.get_winner() != Player.NONE:
                return move
        return None

    def best_evaluated_move(self, game, depth, alpha, beta):
        """ alphaOrig = alpha

        ttEntry = self.transposition_table.get(game)
        if ttEntry is not None and ttEntry.depth >= depth:
            if ttEntry.flag == TTFlag.EXACT:
                return None, ttEntry.value
            elif ttEntry.flag == TTFlag.LOWERBOUND:
                alpha = max(alpha, ttEntry.value)
            elif ttEntry.flag == TTFlag.UPPERBOUND:
                beta = min(beta, ttEntry.value)
            
            if alpha >= beta:
                return None, ttEntry.value """

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

            current_heuristic = -self.best_evaluated_move(current_game, depth-1, -beta, -alpha)[1]
            if current_heuristic > max_heuristic:
                best_move = move
                max_heuristic = current_heuristic

                # only if current_heuristic is greater than max_heuristic, the alpha may change
                alpha = max(alpha, max_heuristic)
                if alpha >= beta:
                    break
        
        """ if max_heuristic <= alphaOrig:
            ttEntry = TranspositionEntry(max_heuristic, depth, TTFlag.UPPERBOUND)
        elif max_heuristic >= beta:
            ttEntry = TranspositionEntry(max_heuristic, depth, TTFlag.LOWERBOUND)
        else:
            ttEntry = TranspositionEntry(max_heuristic, depth, TTFlag.EXACT)
        
        self.transposition_table[game] = ttEntry """
        return (best_move, max_heuristic)
