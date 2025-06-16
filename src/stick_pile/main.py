import os
from importlib import import_module
from pathlib import Path

from competition_controller import CompetitionController
from stick_pile.game import StickPileGame
from game_template.tournament import TemplateTournament
from play_competition import play_competition
from team import Team
from stick_pile.visuals import StickPileGameViewer


def main() -> None:

    function_store = {}

    count = 0

    competitor_code_dir = Path(__file__).parent.resolve() / "competitor_code"
    competitor_code_dir.mkdir(exist_ok=True)

    for entry in os.scandir(competitor_code_dir):

        if (
            entry.is_file()
            and entry.name.startswith("team_")
            and entry.name.endswith(".py")
        ):
            count += 1
            file_name = entry.name.split(".py")[0]
            mod = import_module(file_name, ".competitor_code")
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

    teams = [
        Team(name=name, choose_move_function=function)
        for name, function in function_store.items()
    ]

    controller = CompetitionController(
        "Stick Game",
        teams,
        StickPileGame,
        min_time_per_step=0.4,
        moves_per_state_change=1,
        # speed_increase_factor=2,
    )

    view = StickPileGameViewer(controller=controller)

    play_competition(controller, view)


if __name__ == "__main__":
    main()
