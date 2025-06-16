import math

import pytest

from delta_connect4.game_mechanics import choose_move_randomly as robot_choose_move
from src.connect4.game import Connect4Game
from src.game_parent import PlayState
from src.knockout_competition import KnockoutCompetition, KnockoutCompetitionRound
from src.team import Team


def run_comp_games(comp: KnockoutCompetition):
    while any(game.winner is None for game in comp.live_games):
        [game.step() for game in comp.live_games]


def test_knockout_competition_round():
    comp_round = KnockoutCompetitionRound(
        [Team(f"Robot {n}", robot_choose_move) for n in range(8)], "1st Round", Connect4Game
    )
    assert not comp_round.completed()
    while any(game.winner is None for game in comp_round.games):
        [game.step() for game in comp_round.games]
    assert comp_round.completed()


@pytest.mark.parametrize("num_teams", [3, 5, 7, 8, 9, 13, 33])
def test_knockout_competition_robots_added(num_teams: int):
    comp = KnockoutCompetition(
        [Team(f"Player_{num}", Connect4Game.ROBOT_PLAYER.choose_move) for num in range(num_teams)],
        "Milk Cup",
        Connect4Game,
    )
    expected_num_teams = 2 ** math.ceil(math.log2(num_teams))
    assert len(comp.teams) == expected_num_teams
    for index in range(0, expected_num_teams, 2):
        assert not all(
            [
                comp.teams[index].name == Connect4Game.ROBOT_PLAYER.name,
                comp.teams[index + 1].name == Connect4Game.ROBOT_PLAYER.name,
            ]
        ), "Robot vs robot match!"


def test_knockout_competition_active_rounds_games():
    comp = KnockoutCompetition(
        [Team(f"Robot {n}", Connect4Game.ROBOT_PLAYER.choose_move) for n in range(2)],
        "Connect 4 Cup",
        Connect4Game,
    )
    assert len(comp.live_rounds) == 1
    assert len(comp.live_games) == 1
    assert comp.winner is None


def test_knockout_competition_final_round_completed():
    comp = KnockoutCompetition(
        [Team(f"Robot {n}", Connect4Game.ROBOT_PLAYER.choose_move) for n in range(2)],
        "Connect 4 Cup",
        Connect4Game,
    )
    run_comp_games(comp)
    assert comp.rounds[0].completed()
    assert len(comp.live_rounds) == 1
    assert len(comp.live_games) == 1
    comp.complete_round()
    assert len(comp.live_rounds) == 0
    assert len(comp.live_games) == 0
    assert comp.winner is not None


def test_knockout_competition_10_teams():
    comp = KnockoutCompetition(
        [Team(f"Robot_{n}", robot_choose_move) for n in range(10)],
        "Connect 4 Cup",
        Connect4Game,
    )

    # Round 1, 4 teams playing for 2 places
    assert comp.rounds[-1].name == "1st Round of Connect 4 Cup"
    run_comp_games(comp)
    assert comp.rounds[-1].completed()
    assert comp.rounds[-1].live
    assert comp.rounds[-1].games[0].play_state.value == PlayState.COMPLETED.value
    assert len(comp.live_games) == 8
    comp.complete_round()

    # Round 2, 8 teams
    assert comp.rounds[-1].name == "2nd Round of Connect 4 Cup"
    run_comp_games(comp)
    assert [comp_round.completed() for comp_round in comp.rounds] == [
        True,
        True,
    ]
    assert [comp_round.live for comp_round in comp.rounds] == [False, True]
    assert len(comp.live_games) == 4
    assert len(comp.teams) == 8
    comp.complete_round()
    # Losers removed
    assert len(comp.teams) == 4

    # Semi-Final, 4 teams
    run_comp_games(comp)
    assert [comp_round.completed() for comp_round in comp.rounds] == [True] * len(comp.rounds)
    assert [comp_round.live for comp_round in comp.rounds] == [
        False,
        False,
        True,
    ]
    assert all(game.play_state.value == PlayState.COMPLETED.value for game in comp.rounds[-1].games)
    assert len(comp.live_games) == 2
    assert len(comp.teams) == 4
    comp.complete_round()
    # Losers aren't removed - 3rd/4th playoff!
    assert len(comp.teams) == 4

    # Final & 3rd/4th playoff, 4 teams in total
    run_comp_games(comp)
    assert all(comp_round.completed() for comp_round in comp.rounds)

    live_rounds = [comp_round.live for comp_round in comp.rounds]
    assert live_rounds[:3] == [False, False, False]
    assert len(live_rounds) == 5
    assert all(game.play_state.value == PlayState.COMPLETED.value for game in comp.rounds[-1].games)
    assert len(comp.live_games) >= 1
    assert len(comp.teams) == 4
    comp.complete_round()


def test_robot_vs_robot_games_skipped():
    round_of_games = KnockoutCompetitionRound(
        [Connect4Game.ROBOT_PLAYER] * 8,
        "Connect 4 Cup",
        Connect4Game,
    )

    assert all(game.completed for game in round_of_games.games)


def test_robot_only_comps() -> None:

    comp = KnockoutCompetition(
        [Connect4Game.ROBOT_PLAYER] * 8,
        "Connect 4 Cup",
        Connect4Game,
    )
    assert comp.winner == Connect4Game.ROBOT_PLAYER
