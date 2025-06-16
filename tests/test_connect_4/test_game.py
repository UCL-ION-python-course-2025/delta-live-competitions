from time import sleep

import numpy as np
import pytest

from delta_connect4.game_mechanics import choose_move_randomly as robot_choose_move
from src.connect4.game import Connect4Game
from src.team import Team


def test_take_turn():
    game = Connect4Game(
        Team("Robot 1", robot_choose_move),
        Team("Robot 2", robot_choose_move),
        "Test Match (not cricket)",
    )
    game.step()
    assert np.any(game.board != 0)


def test_reset_game():
    game = Connect4Game(
        Team("Robot 1", robot_choose_move),
        Team("Robot 2", robot_choose_move),
        "Test Match (not cricket)",
    )
    game.step()
    assert np.any(game.board != 0)
    game.reset_game()
    assert np.all(game.board == 0)


def test_winner_loser():
    team_2 = Team("Robot 2", robot_choose_move)
    game = Connect4Game(Connect4Game.ROBOT_PLAYER, team_2, "Test Match (not cricket)")

    # loop to ensure the game doesn't end in a draw
    while game.winner is None:
        if game.completed:
            game.reset_game()
        game.step()

    assert game.winner in [Connect4Game.ROBOT_PLAYER, team_2]
    assert game.loser in [Connect4Game.ROBOT_PLAYER, team_2]


def test_take_move_timeout_works() -> None:

    # I cannot catch the TimeoutException directly for some reason
    # so just need to check for general exception
    with pytest.raises(Exception):

        def slow_move(state: np.ndarray):
            sleep(1.1)
            return np.random.randint(0, 7)

        team1 = Team("Slow player", slow_move)
        team2 = Team("Slow player", slow_move)
        team1.timeout = 1
        team2.timeout = 1
        game = Connect4Game(
            team1,
            team2,
            "Test Match (not cricket)",
        )

        game.step()

    # Make sure there are no other exceptions
    team1 = Team("Slow player", slow_move)
    team2 = Team("Slow player", slow_move)
    team1.timeout = 2
    team2.timeout = 2
    game = Connect4Game(
        team1,
        team2,
        "Test Match (not cricket)",
    )

    game.step()
