import sys
from pathlib import Path

import delta_shooter
from competition_controller import CompetitionController
from play_competition import play_competition
from team import Team

# makes e.g. "import game_mechanics" available to competitor code files
sys.path.append(delta_shooter.__path__[0])  # isort:skip
from delta_shooter.game_mechanics import load_network  # isort:skip
from shooter.game import ShooterGame  # isort:skip
from shooter.visuals import ShooterGameViewer  # isort:skip


def main() -> None:
    function_store = {}

    count = 0
    competitor_code_dir = Path(__file__).parent.resolve() / "competitor_code"
    competitor_code_dir.mkdir(exist_ok=True)
    for entry in competitor_code_dir.iterdir():

        if entry.is_file() and entry.name != "__init__.py" and entry.name.endswith(".py"):
            count += 1
            file_name = entry.name.split(".py")[0]
            if not file_name.startswith("team_"):
                continue
            mod = __import__(f"shooter.competitor_code.{file_name}", fromlist=["None"])
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

            # This try-except imports any necessary user-defined classes
            try:
                if (competitor_code_dir / f"{team_name}_network.pt").exists():
                    network = load_network(team_name, competitor_code_dir)
                else:
                    network = None
            except AttributeError as e:
                # TODO: This only works for unique class names
                # Grab the classname from the error message
                user_defined_class_name = e.args[0].split("'")[2]
                # Import the class
                user_defined_class = getattr(mod, user_defined_class_name)
                # Add the class to the local namespace so it can be used in the unpickling
                globals()[user_defined_class_name] = user_defined_class

                network = load_network(team_name, competitor_code_dir)

            function_store[team_name] = func, network

    controller = CompetitionController(
        "Delta Academy Space Shooter Competition",
        [
            Team(name, function, neural_network=neural_network)
            for name, (function, neural_network) in function_store.items()
        ],
        ShooterGame,
        min_time_per_step=0.1,
    )

    view = ShooterGameViewer(controller=controller)

    play_competition(controller, view)


if __name__ == "__main__":
    main()
