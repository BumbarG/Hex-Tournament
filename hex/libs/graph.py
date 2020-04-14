from collections import defaultdict

import numpy as np
import heapdict

from system.enums import Player
from system.state import State


def find_shortest_path_Dijkstra(player, game: State):
    '''
    returns the distance (int, min number of steps) between start (hex) and end (hex) in the game.
    active_player ... not same as active player. 
    game ... instance of State ... contains the tile graph and the player who is currently active.
    start ... the starting cell.
    end ... the target cell.
    if the function returns np.inf, then no path was found and a player should have already been declared the winnder.
    '''
    Q = heapdict()
    # prev = defaultdict(None) # we dont need the path
    dist = defaultdict(lambda x: np.inf)
    for i in range(game.size):
        for j in range(game.size):
            Q[(i, j)] == np.inf
    if player == Player.WHITE:
        Q[(-1, None)] = 0
        dist[(-1, None)] = 0

    if player == Player.BLACK:
        Q[(None, -1)] = 0
        dist[(None, -1)] = 0

    while (len(Q) > 0):
        u = Q.popitem()
        if is_target(u[0], player, game.size):
            return u[1]
        for neighbour in get_neighbours(u[0], game.size):
            if neighbour in Q:
                alt = u[1] + length(u[0], neighbour, game.board)
                if alt < dist[neighbour]:
                    dist[neighbour] = alt
                    Q[neighbour] = alt
                    # prev[neighbour] = u[0] # we dont need the path

    raise Exception('Function should terminate beforehand.')


def length(a, b, board):
    if board[a[0], a[1]] == board[b[0], b[1]]:
        return 0
    if (board[a[0], a[1]] == Player.NONE.value) or (board[b[0], b[1]] == Player.NONE.value):
        return 1
    else:
        return np.inf


def is_target(u, player, size):
    if player == Player.WHITE and u[0] == size-1:
        return True
    if player == Player.BLACK and u[1] == size-1:
        return True
    else:
        return False


def get_neighbours(cell, size):
    if cell[0] == -1:
        return [(0, i) for i in range(size)]
    if cell[1] == -1:
        return [(i, 0) for i in range(size)]
    else:
        return [(cell[0] + n[0], cell[1] + n[1]) for n in ((-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, -1))
                if (0 <= cell[0] + n[0] < size and 0 <= cell[1] + n[1] < size)]
