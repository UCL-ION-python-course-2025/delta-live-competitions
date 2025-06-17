import random
from typing import Any, Callable, Dict, Literal, Tuple
import time


def choose_move_randomly(number_of_sticks_remaining) -> int:
    if number_of_sticks_remaining < 3:
        return random.choice(list(range(1, number_of_sticks_remaining + 1)))
    return random.choice([1, 2, 3])


class Player:
    """This class defines which players turn it is.

    If player: It is the turn of the player passing action directly to step.  If opponent: It is the
    turn of the opponent_choose_move function passed  to WildTictactoeEnv's __init__()
    """

    player = "player"
    opponent = "opponent"


def play_game(
    your_choose_move: Callable,
    opponent_choose_move: Callable,
    game_speed_multiplier=1,
):

    game = StickPile(
        opponent_choose_move=opponent_choose_move,
        game_speed_multiplier=game_speed_multiplier,
        verbose=True,
        render=False,
    )

    state, reward, done, info = game.reset()
    while not done:

        action = your_choose_move(state)
        state, reward, done, info = game.step(action)


class StickPile:
    def __init__(
        self,
        opponent_choose_move: Callable,
        game_speed_multiplier=1,
        verbose=False,
        render=True,
    ) -> None:
        """Initialises the object.

        Is called when you call `environment = Env()`.

        It sets everything up in the starting state for the episode to run.
        """
        self.opponent_choose_move = opponent_choose_move
        self.game_speed_multiplier = game_speed_multiplier
        self.verbose = verbose
        self.render = render

    def reset(self, take_first_step: bool = True) -> Tuple[Any, float, bool, Dict]:
        """Resets the environment (resetting state, total return & whether the episode has
        terminated) so it can be re-used for another episode.

        Returns:
            Same type output as .step(). Tuple of:
                1. state (Any): The state after resetting the environment
                2. reward (None): None at this point, since no reward is
                   given initially
                3. done (boolean): Always `True`, since the episode has just
                   been reset
                4. info (dict): Dictionary of any extra information
        """

        self.number_of_sticks_remaining = random.randint(15, 25)
        if self.verbose:
            print(f"Game starting with {self.number_of_sticks_remaining} sticks")
        self.player_move: Literal["player", "opponent"] = random.choice(
            ["player", "opponent"]
        )
        self.done: bool = False

        if self.player_move == "opponent" and take_first_step:
            opponent_action = self.opponent_choose_move(
                number_of_sticks_remaining=self.number_of_sticks_remaining
            )
            self._step(opponent_action)

        return self.number_of_sticks_remaining, 0, self.done, {}

    def step(self, action: Any) -> Tuple[Any, float, bool, Dict]:
        """
        Given an action to take:
            1. sample the next state and update the state
            2. get the reward from this timestep
            3. determine whether the episode has terminated

        Args:
            action: The action to take. Determined by user code
                that runs the policy

        Returns:
            Tuple of:
                1. state (Any): The updated state after taking the action
                2. reward (float): Reward at this timestep
                3. done (boolean): Whether the episode is over
                4. info (dict): Dictionary of extra information
        """
        reward = self._step(action)

        if not self.done:
            opponent_action = self.opponent_choose_move(self.number_of_sticks_remaining)
            opponent_reward = self._step(opponent_action)
            reward = -1 * opponent_reward

        if reward == 1 and self.verbose:
            print("Well done, you took the last stick! You win!")
        elif reward == -1 and self.verbose:
            print("Oh no! Your opponent took the last stick! You lose!")
        return self.number_of_sticks_remaining, reward, self.done, {}

    def _step(self, num_sticks_remove: int) -> int:
        if self.verbose:
            time.sleep(0.5 / self.game_speed_multiplier)
            print("\n")

        msg, is_valid = self.move_is_valid(num_sticks_remove)
        if not is_valid:
            print(msg)
            print("\nGame Terminated")
            self.done = True
            return -1

        self.number_of_sticks_remaining -= num_sticks_remove
        if self.verbose:
            print(
                f"{self.player_move.capitalize()} removed {num_sticks_remove} stick{'s' if num_sticks_remove != 1 else ''}"
            )
            print(
                f"There {"are" if self.number_of_sticks_remaining != 1 else "is"} {self.number_of_sticks_remaining} stick{'s' if self.number_of_sticks_remaining != 1 else ''} left"
            )

        if self.number_of_sticks_remaining == 0:
            self.done = True
            return 1

        self.switch_player()

        return 0

    def switch_player(self) -> None:
        self.player_move = "opponent" if self.player_move == "player" else "player"

    def move_is_valid(self, num_sticks_remove: int) -> Tuple[str, bool]:
        player_indicator_string = (
            "Your" if self.player_move == "player" else "Your opponent's"
        )
        if num_sticks_remove is None:
            return (
                f"Whoops {player_indicator_string} function did not return anything! Your function must return 1, 2, or 3.",
                False,
            )
        if not isinstance(num_sticks_remove, int):
            return (
                f"Whoops. {player_indicator_string} function did not return an integer! {player_indicator_string} function returned {num_sticks_remove}.",
                False,
            )

        player_indicator_string = (
            "You" if self.player_move == "player" else "Your opponent"
        )
        if num_sticks_remove not in [1, 2, 3]:

            return (
                f"Only 1, 2, or 3 sticks can be removed at any time! {player_indicator_string} tried to remove {num_sticks_remove} sticks",
                False,
            )

        if num_sticks_remove > self.number_of_sticks_remaining:
            return (
                f"Invalid move! {player_indicator_string} tried to remove {num_sticks_remove} sticks, but there {"are" if self.number_of_sticks_remaining != 1 else "is"} only {self.number_of_sticks_remaining} stick{'s' if self.number_of_sticks_remaining != 1 else ''} remaining.",
                False,
            )
        return "", True
