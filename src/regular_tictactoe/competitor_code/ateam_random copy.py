import random

import numpy as np

from game_mechanics import (
    choose_move_randomly,
    human_player,
    play_ttt_game,
)

TEAM_NAME = "Team random" + str(
    random.choice(list(range(100)))
)  # <---- Enter your team name here!
assert TEAM_NAME != "Team Name", "Please change your TEAM_NAME!"


def choose_move(board) -> int:
    return random.choice([idx for idx, square in enumerate(board) if square == 0])


if __name__ == "__main__":

    # Play against your bot!!
    play_ttt_game(
        your_choose_move=choose_move,
        opponent_choose_move=choose_move_randomly,
        game_speed_multiplier=10,
        verbose=True,
        render=False,
    )
