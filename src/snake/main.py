import os
from pathlib import Path

from competition_controller import CompetitionController
from play_competition import play_competition
from snake import SnakeGame
from snake.visuals import SnakeGameViewer
from team import Team

if __name__ == "__main__":
    function_store = {}

    count = 0

    competitor_code_dir = Path(__file__).parent.resolve() / "competitor_code"
    competitor_code_dir.mkdir(exist_ok=True)

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
    controller = CompetitionController(
        "Delta Academy Snake Competition",
        [Team(name, function) for name, function in function_store.items()],
        SnakeGame,
        0.5,
    )

    view = SnakeGameViewer(controller=controller)

    play_competition(controller, view)
