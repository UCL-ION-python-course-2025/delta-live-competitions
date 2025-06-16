import sys
from pathlib import Path

import delta_go
from competition_controller import CompetitionController
from play_competition import play_competition
from team import Team

# makes e.g. "import game_mechanics" available to competitor code files
sys.path.append(delta_go.__path__[0])  # isort:skip

from go.game import GoGame  # isort:skip
from go.visuals import GoGameViewer  # isort:skip
from delta_go.game_mechanics import load_pkl  # isort:skip


def main() -> None:
    function_store = {}

    count = 0

    competitor_code_dir = Path(__file__).parent.resolve() / "competitor_code"
    competitor_code_dir.mkdir(exist_ok=True)
    for team_folder in competitor_code_dir.iterdir():

        if team_folder.is_dir() and team_folder.name.startswith("team"):
            count += 1

            main_path = team_folder / "main.py"
            assert main_path.exists(), f"main.py not found in {team_folder}"

            sys.path.append(str(team_folder))
            mod = __import__(
                f"go.competitor_code.{team_folder.name}.main", fromlist=["None"]
            )
            sys.path.remove(str(team_folder))

            try:
                func = getattr(mod, "choose_move")
            except AttributeError as e:
                raise AttributeError(
                    f"No function 'choose_move' found in file {main_path}"
                ) from e
            try:
                team_name = getattr(mod, "TEAM_NAME")
            except AttributeError as e:
                raise AttributeError(f"No TEAM_NAME found in file {main_path}") from e

            if len(team_name) == 0:
                raise ValueError(f"TEAM_NAME is empty in file {main_path}")

            # Use pathlib to check if a file with a .pkl extension exists
            if not any(team_folder.glob("*.pkl")):
                print(f"No .pkl file found in {team_folder} - setting to None")
                pkl = {}
            else:
                # This try-except imports any necessary user-defined classes
                try:
                    pkl = load_pkl(team_name, team_folder)
                except AttributeError as e:
                    # TODO: This only works for unique class names
                    # Grab the classname from the error message
                    user_defined_class_name = e.args[0].split("'")[2]
                    # Import the class
                    user_defined_class = getattr(mod, user_defined_class_name)
                    # Add the class to the local namespace so it can be used in the unpickling
                    globals()[user_defined_class_name] = user_defined_class
                    pkl = load_pkl(team_name, competitor_code_dir)

            try:
                MctsClass = getattr(mod, "MCTS")
            except AttributeError:
                MctsClass = None

            function_store[team_name] = func, pkl, MctsClass

    controller = CompetitionController(
        "Delta Academy Go Competition",
        [
            Team(name, function, pkl_file=pkl_file, MctsClass=MctsClass)
            for name, (function, pkl_file, MctsClass) in function_store.items()
        ],
        GoGame,
        min_time_per_step=1,
        moves_per_state_change=1,
    )

    view = GoGameViewer(controller=controller)

    play_competition(controller, view)


if __name__ == "__main__":
    main()
