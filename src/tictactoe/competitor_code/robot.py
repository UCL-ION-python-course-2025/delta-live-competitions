"""THE FILE YOU WRITE!"""
import math
import random
from typing import List

import numpy as np

from game_mechanics import play_tic_tac_toe


def choose_move(board: List[int]):  # <-- Leave this alone!
    """YOU WRITE THIS FUNCTION.

    Decide where to play next!

    Args:
        board: list representing the board.

            Elements which are 0 are empty spaces.
            Elements which are 1 are YOUR crosses.
            Elements which are -1 are THE OPPONENT's noughts.

        Example input: [0, 0, 1, -1, 0, 1, -1, 0, 0]
            Where above represents:

                |   | X
             -----------
              O |   | X
             -----------
              O |   |

    Returns:
        The index you want to place your piece in (an integer 0 -> 8)
    """
    return random.choice([count for count, item in enumerate(board) if item == 0])


if __name__ == "__main__":
    play_tic_tac_toe(choose_move)
