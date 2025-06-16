import os
import random
import sys
from pathlib import Path

import numpy as np

import delta_tron
import torch
from competition_controller import CompetitionController
from play_competition import play_competition
from team import Team

# makes e.g. "import game_mechanics" available to competitor code files
sys.path.append(delta_tron.__path__[0])  # isort:skip
from tron.game import TronGame  # isort:skip
from tron.visuals import TronGameViewer  # isort:skip


def main() -> None:
    seed = random.randint(0, 100)
    print(f"Random seed: {seed}")
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)

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
            mod = __import__(f"tron.competitor_code.{file_name}", fromlist=["None"])
            try:
                func = getattr(mod, "choose_move")
            except AttributeError as e:
                raise Exception(f"No function 'choose_move' found in file {file_name}") from e
            try:
                team_name = getattr(mod, "TEAM_NAME")
            except AttributeError as e:
                raise Exception(f"No TEAM_NAME found in file {file_name}") from e
            try:
                mcts = getattr(mod, "MCTS")
            except AttributeError as e:
                raise Exception(f"No MCTS class found in file {file_name}") from e

            if len(team_name) == 0:
                raise ValueError(f"TEAM_NAME is empty in file {file_name}")

            function_store[team_name] = func, mcts

    controller = CompetitionController(
        "Delta Academy Tron Competition",
        [
            Team(name, choose_move, MctsClass=mcts)
            for name, (choose_move, mcts) in function_store.items()
        ],
        TronGame,
        min_time_per_step=0.2,
        moves_per_state_change=1,
    )

    view = TronGameViewer(controller=controller)

    play_competition(controller, view)


if __name__ == "__main__":
    main()
