from abc import ABC, abstractmethod
from typing import List, Type

from game_parent import Game
from team import Team


class Competition(ABC):
    def __init__(self, teams: List[Team], name: str, game: Type[Game]):
        assert len(teams) > 0, "Must be some teams!"
        self.teams = teams
        self.game = game
        self.name = name

    @property
    @abstractmethod
    def winner(self) -> Team:
        pass

    @property
    @abstractmethod
    def ranking(self) -> Team:
        pass

    @property
    @abstractmethod
    def live_games(self) -> List[Game]:
        pass
