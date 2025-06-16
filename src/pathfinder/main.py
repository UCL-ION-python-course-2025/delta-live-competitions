import os

from competition_controller import CompetitionController
from pathfinder.game import PathfinderGame
from pathfinder.visuals import PathfinderGameViewer
from play_competition import play_competition
from team import Team


def main() -> None:
    function_store = {}

    count = 0
    competitor_code_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "competitor_code"
    )
    for entry in os.scandir(competitor_code_dir):

        if entry.is_file() and entry.name != "__init__.py" and entry.name.endswith(".py"):
            count += 1
            file_name = entry.name.split(".py")[0]
            if not file_name.startswith("team_"):
                continue
            mod = __import__(f"competitor_code.{file_name}", fromlist=["None"])
            try:
                func = getattr(mod, "choose_move")
            except AttributeError as e:
                raise Exception(f"No function 'choose_move' found in file {file_name}") from e
            try:
                team_name = getattr(mod, "TEAM_NAME")
            except AttributeError as e:
                raise Exception(f"No TEAM_NAME found in file {file_name}") from e

            if len(team_name) == 0:
                raise ValueError(f"TEAM_NAME is empty in file {file_name}")

            function_store[team_name] = func

    # Set me up for each game
    controller = CompetitionController(
        "Pathfinder Competition",
        [Team(name, function) for name, function in function_store.items()],
        PathfinderGame,
        min_time_per_step=0.1,
    )
    view = PathfinderGameViewer(controller=controller)

    play_competition(controller, view)


if __name__ == "__main__":
    main()
