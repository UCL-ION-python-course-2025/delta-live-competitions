import random

from .game_mechanics import play_pathfinder

TEAM_NAME = "Robot"
# UNCOMMENT WHEN IN REPLIT
# import replit
# replit.clear()
"""
YOUR FIRST TASK: Write code that loads the csv file 'board.csv' into a numpy array

Next, you need to follow the path to the goal through the 2D array.

Look at board.csv
"""


def choose_move(board, position):
    """YOU WRITE THIS FUNCTION.

    Decide where to play next!

    Args:
        board: the path to a csv file that contains the maze

            Elements which are 0 are empty spaces.
            Elements which are 1 are THE PATH.
            Elements which are 2 you have already visited.

    Returns:
        A tuple (x, y) of the next move to take
    """
    # Create a list of lists with different moves you could take (N, S, E, W)
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    possible_moves = []

    # Check if the move stays within the board
    for m in moves:

        new_pos = [int(position[0] + m[0]), int(position[1] + m[1])]

        if 0 <= new_pos[0] <= 9 and 0 <= new_pos[1] <= 9:
            possible_moves.append(m)

    return random.choice(possible_moves)


# board = ...  # <- this is where you write the code that loads the csv

# Line below plays the pathfinder game!
# play_pathfinder(board, choose_move)
