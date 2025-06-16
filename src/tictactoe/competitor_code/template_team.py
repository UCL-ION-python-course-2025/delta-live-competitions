import random
from typing import Dict, List

from game_mechanics import TictactoeMechanics, load_dictionary, render, save_dictionary

TEAM_NAME = "TEAM NAME"  # <---- Enter your team name here!

MODE = "Train"  # <------- Start here, set mode to train to train your algorithm!
# MODE = "Test"  # <----- Test your algorithm here with a graphical game against a randomly moving opponent
#                          (you play as "X")


def train(game) -> Dict:
    """Write this function to train your algorithm!

    Arg:
        game:
            The environment that you will interact with to play tictactoe.
            The game environment has two functions you will need to call, step and reset.
    Functions:
        reset: starts a new game with a clean board, randomly choose the first player
                to go first.
        step:  Make a move on the current board.
    Variables:
        Both reset and step return the same 4 variables --
        observation (List[int]): The state of the board as a list of ints (see choose_move)
        reward [1, 0 or None]: The reward from the environment after the current move.
                               1 = win, 0 = draw/lose, None = no winner on this turn
        done (bool): True if the game is over, False otherwise.
        info (dict): Additional information about the current state of the game.
                     "winner" (Cell): the winner of the game, if there is one.
                     "player_move" (Cell): the player who just moved.

    Returns:
        A dictionary containing data to be used by your agent during gameplay.
        You can structure this however you like as long as you write a
        choose_move function that can use it.
    """

    # An example training function that plays one game moving randomly, then returns
    # an empty dictionary.
    observation, reward, done, info = game.reset()
    while not done:
        # TODO: This is currently deciding both X and O moves, is this ok?
        next_move = choose_move(observation, {})
        observation, reward, done, info = game.step(next_move, verbose=False)

    return {}


def choose_move(board: List, my_dict: Dict) -> int:
    """This function will be called during competitive play. It will take the current state of the
    board. You will need to return a single move to play on this board.

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

        my_dict: The dictionary you saved in your training function.

    Returns:
        The index you want to place your piece in (an integer 0 -> 8)
    """
    return random.choice([count for count, item in enumerate(board) if item == 0])


if __name__ == "__main__":

    if MODE == "Train":
        my_dict = train(TictactoeMechanics())
        save_dictionary(my_dict, TEAM_NAME)
    elif MODE == "Test":
        my_dict = load_dictionary(TEAM_NAME)
        render(choose_move, my_dict)
    else:
        raise ValueError("MODE must be either Train or Test")
