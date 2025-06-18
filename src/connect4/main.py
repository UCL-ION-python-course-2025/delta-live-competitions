import os
import sys
from pathlib import Path

import delta_connect4
from competition_controller import CompetitionController
from connect4.game import Connect4Game
from connect4.visuals import Connect4GameViewer
from delta_connect4.game_mechanics import load_dictionary
from play_competition import play_competition
from team import Team

# makes e.g. "import game_mechanics" available to competitor code files
sys.path.append(delta_connect4.__path__[0])  # isort:skip


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
            mod = __import__(f"competitor_code.{file_name}", fromlist=["None"])
            try:
                func = getattr(mod, "choose_move")
            except AttributeError as e:
                raise Exception(
                    f"No function 'choose_move' found in file {file_name}"
                ) from e
            try:
                team_name = getattr(mod, "TEAM_NAME")
            except AttributeError as e:
                raise Exception(f"No TEAM_NAME found in file {file_name}") from e

            if len(team_name) == 0:
                raise ValueError(f"TEAM_NAME is empty in file {file_name}")

            function_store[team_name] = func

    controller = CompetitionController(
        "Delta Academy Connect-4 Competition",
        [Team(name, function) for name, function in function_store.items()],
        Connect4Game,
        min_time_per_step=1,
        moves_per_state_change=1,
        plate_enabled=False,
    )

    view = Connect4GameViewer(controller=controller)

    play_competition(controller, view)


if __name__ == "__main__":
    main()
