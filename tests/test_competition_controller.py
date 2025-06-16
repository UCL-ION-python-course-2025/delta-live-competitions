import math

import pytest

from delta_connect4.game_mechanics import choose_move_randomly as robot_choose_move
from src.competition_controller import CompetitionController
from src.connect4.game import Connect4Game
from src.team import Team


def test_imports():  # Placeholder
    pass


@pytest.mark.parametrize("num_teams", [5, 10, 15, 20])
def test_competition_controller_run_all_games(num_teams: int):
    controller = CompetitionController(
        "Delta Academy Connect-4 Competition",
        [Team(f"Player{str(n).zfill(num_teams)}", robot_choose_move) for n in range(num_teams)],
        Connect4Game,
        0,
    )
    # This turns off waiting to keep moves from happening too fast
    while controller.competitions[0].winner is None:
        controller.run_round_of_games()
        if controller.competitions[0].winner is None:
            controller.new_round()
    assert all(
        comp_round.completed() for comp in controller.competitions for comp_round in comp.rounds
    )
    biggest_round_size = 2 ** math.ceil(math.log2(num_teams / 2))
    expected_num_games = (
        [biggest_round_size] * 2
        + [
            biggest_round_size // (2**i)
            for i in range(1, round(math.log2(biggest_round_size) - 1))
        ]
        + [3, 1]
    )

    # Check the expected number of games in each round
    num_games = [len(games) for games in controller.rounds_of_games]
    assert all(num <= exp for num, exp in zip(num_games, expected_num_games))

    # Check the worst rank (highest number) is less than or equal to the number of teams
    assert max(controller.ranking.keys()) <= num_teams

    # Check the number of teams in the ranking dict is equal to the number of unique teams (no repeated teams)
    assert (
        sum(len(teams) for teams in controller.ranking.values())
        == len({entry.team_id for team_list in controller.ranking.values() for entry in team_list})
        <= num_teams  # <= because draws reduce the number of teams in the rankings
    )
