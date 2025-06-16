import numpy as np

from game_mechanics import play_pathfinder


def choose_move(board, position):
    """YOU WRITE THIS FUNCTION.

    Decide where to play next!

    Args:
        board: the path to a csv file that contains the maze

            Elements which are 0 are empty spaces.
            Elements which are 1 are THE PATH.
            Elements which are 2 have already been travelled on.

    Returns:
        A list [x, y] of the next move to take
    """
    # Create a list of lists with different moves you could take (N, S, E, W)

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    possible_moves = [
        m for m in moves if 0 <= position[0] + m[0] <= 9 and 0 <= position[1] + m[1] <= 9
    ]

    for move in possible_moves:
        if board[position[0] + move[0], position[1] + move[1]] == 1:
            return move


board_path = "./board.csv"
board = np.loadtxt(board_path, delimiter=",")

play_pathfinder(board, choose_move)
