import numpy as np

from libs.graph import find_shortest_path_Dijkstra
from system.enums import Player
from system.state import State


def shortest_connecting_path_length(game: State):
    '''
    returns the difference between the length of our shortest connecting path and the length
    of the opponents shortest connecting path.
    Goes over all cells of the active player and calculates the minimum distanceb between them and all the target tiles.
    '''
    if game.get_winner() != Player.NONE:  # I don't think we can get opposing player as the winner here. Might need to change.
        return np.inf
    if game.player == Player.WHITE:
        # the below could perhaps be a weighted sum.
        return -find_shortest_path_Dijkstra(Player.WHITE, game)+find_shortest_path_Dijkstra(Player.BLACK, game)
    if game.player == Player.BLACK:
        # the below could perhaps be a weighted sum.
        return -find_shortest_path_Dijkstra(Player.BLACK, game)+find_shortest_path_Dijkstra(Player.WHITE, game)
    raise Exception('Function should not reach this.')
