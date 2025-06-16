import enum
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4

import numpy as np

try:
    from torch import nn
except ModuleNotFoundError:

    class FakeNN:
        def Module(self) -> None:
            pass

    nn = FakeNN


from timeout import timeout


class Outcome(enum.Enum):
    LOSE = -1
    DRAW = 0
    WIN = 1


class Team:
    def __init__(
        self,
        name: str,
        choose_move_function: Callable,
        value_function: Optional[Dict] = None,
        neural_network: Optional[nn.Module] = None,
        pkl_file: Optional[Any] = None,
        MctsClass: Optional[type] = None,
    ):
        self.team_id = uuid4()
        self.name = name
        self._choose_move_function = choose_move_function
        self.results: List[Result] = []
        self.timeout = 10
        self.value_function = value_function
        self.neural_network = neural_network
        self.pkl_file = pkl_file
        self.MctsClass = MctsClass
        # initialised instance of the team's MCTS class
        self.mcts = MctsClass() if MctsClass is not None else None

    def __repr__(self) -> str:
        return f"Team: {self.name}"

    def __eq__(self, other) -> bool:
        return isinstance(other, Team) and self.team_id == other.team_id

    def already_played(self) -> List["Team"]:
        return [result.opponent for result in self.results]

    def final_result(self) -> str:
        win_lose = "Winner of" if self.results[-1].outcome == Outcome.WIN else "Lost "
        return f"{win_lose} {self.results[-1].match_name}"

    def choose_move(self, **kwargs: Any) -> Any:
        if self.value_function is not None:
            kwargs["value_function"] = self.value_function
        if self.neural_network is not None:
            kwargs["neural_network"] = self.neural_network
        if self.pkl_file is not None:
            kwargs["pkl_file"] = self.pkl_file
        if self.mcts is not None:
            kwargs["mcts"] = self.mcts

        @timeout(self.timeout)
        def move_with_timeout(self: Team, **kwargs: Any) -> None:
            return self._choose_move_function(**kwargs)

        return move_with_timeout(self, **kwargs)


@dataclass
class Result:
    final_board: np.ndarray
    outcome: Outcome
    match_name: str
    opponent: Team
