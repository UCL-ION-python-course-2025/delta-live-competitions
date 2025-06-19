import os
import sys
from importlib import import_module
from pathlib import Path

import delta_tictactoe
from competition_controller import CompetitionController
from delta_tictactoe.game_mechanics import load_dictionary
from play_competition import play_competition
from team import Team

from regular_tictactoe.game import TicTacToeGame
from regular_tictactoe.visuals import WildTictactoeGameViewer

# makes e.g. "import game_mechanics" available to competitor code files
sys.path.append(delta_tictactoe.__path__[0])  # isort:skip


def main() -> None:

    function_store = {}

    count = 0
    competitor_code_dir = Path(__file__).parent.resolve() / "competitor_code"
    competitor_code_dir.mkdir(exist_ok=True)
    for entry in os.scandir(competitor_code_dir):

        if (
            entry.is_file()
            and entry.name != "__init__.py"
            and entry.name.endswith(".py")
        ):
            count += 1
            file_name = entry.name.split(".py")[0]
            if not file_name.startswith("team_"):
                continue
            mod = __import__(
                f"regular_tictactoe.competitor_code.{file_name}", fromlist=["None"]
            )

            try:
                func = getattr(mod, "choose_move")
            except AttributeError as e:
                raise Exception(
                    f"No function 'choose_move' found in file {file_name}"
                ) from e
            try:
                team_name = getattr(mod, "TEAM_NAME")
                print("Loading in: ", team_name)
            except AttributeError as e:
                raise Exception(f"No TEAM_NAME found in file {file_name}") from e

            if len(team_name) == 0:
                raise ValueError(f"TEAM_NAME is empty in file {file_name}")
            function_store[team_name] = func

    teams = [
        Team(name=name, choose_move_function=func)
        for name, func in function_store.items()
    ]

    controller = CompetitionController(
        "Tic-Tac-Toe",
        teams,
        TicTacToeGame,
        min_time_per_step=0.1,
        moves_per_state_change=1,
        plate_enabled=False,
    )
    tournament_view = WildTictactoeGameViewer(controller)
    play_competition(controller, view=tournament_view)


if __name__ == "__main__":
    main()
