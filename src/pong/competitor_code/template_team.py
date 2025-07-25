import random
from typing import Optional, Tuple

import numpy as np
import torch
from torch import nn

from check_submission import check_submission
from game_mechanics import PongEnv, load_network, play_pong, robot_choose_move, save_network

TEAM_NAME = "Team Name"  # <---- Enter your team name here!
assert TEAM_NAME != "Team Name", "Please change your TEAM_NAME!"


def train() -> nn.Module:
    """
    TODO: Write this function to train your algorithm.

    Returns:
        A pytorch network to be used by choose_move. You can architect
        this however you like but your choose_move function must be able
        to use it.
    """
    raise NotImplementedError("You need to implement this function!")


def choose_move(
    state: np.ndarray,
    neural_network: nn.Module,
) -> int:  # <--------------- Please do not change these arguments!
    """Called during competitive play. It acts greedily given current state of the board and value
    function dictionary. It returns a single move to play.

    Args:
        state: State of the game as a np array, length = 5.
        network: The pytorch network output by train().

    Returns:
        move (int): The move you want to given the state of the game.
                    Should be in {-1,0,1}.
    """
    raise NotImplementedError("You need to implement this function!")


if __name__ == "__main__":

    ## Example workflow, feel free to edit this! ###
    my_network = train()
    save_network(my_network, TEAM_NAME)
    my_network = load_network(TEAM_NAME)

    #  Code below plays a single game of pong against a basic robot player
    #  opponent, think about how you might want to adapt this to
    #  test the performance of your algorithm.
    def choose_move_no_network(state) -> int:
        """The arguments in play_pong_game() require functions that only take the state as input.

        This converts choose_move() to that format.
        """
        return choose_move(state, neural_network=my_network)

    play_pong(
        your_choose_move=choose_move_no_network,
        opponent_choose_move=robot_choose_move,
        game_speed_multiplier=1,
        verbose=True,
    )

    # Uncomment line below to check your submission works
    # check_submission()
