import os
from importlib import import_module
from pathlib import Path

from competition_controller import CompetitionController
from play_competition import play_competition
from stock_market.game import StockGame
from team import Team
from tournament import StockTournament


def main() -> None:

    function_store = {}

    count = 0
    competitor_code_dir = Path(__file__).parent.resolve() / "competitor_code"
    competitor_code_dir.mkdir(exist_ok=True)
    for entry in os.scandir(competitor_code_dir):

        if entry.is_file() and entry.name.startswith("team_") and entry.name.endswith(".py"):
            count += 1
            file_name = entry.name.split(".py")[0]
            mod = import_module(file_name, ".competitor_code")
            try:
                func = getattr(mod, "predict_price")
            except AttributeError as e:
                raise Exception(f"No function 'predict_price' found in file {file_name}") from e
            try:
                team_name = getattr(mod, "TEAM_NAME")
            except AttributeError as e:
                raise Exception(f"No TEAM_NAME found in file {file_name}") from e

            if len(team_name) == 0:
                raise ValueError(f"TEAM_NAME is empty in file {file_name}")

            function_store[team_name] = func

    teams = [
        Team(name=name, choose_move_function=function) for name, function in function_store.items()
    ]

    controller = CompetitionController(
        "", teams, StockGame, min_time_per_step=1, moves_per_state_change=1
    )
    tournament_view = StockTournament(controller)
    play_competition(controller, view=tournament_view)


if __name__ == "__main__":
    main()
