from typing import Dict, List, Optional, Type

import numpy as np

from competition import Competition
from game_parent import Game, MultiPlayerGame, PointsGame
from team import Team


class MultiplayerCompetition(Competition):
    def __init__(self, teams: List[Team], name: str, game: Type[MultiPlayerGame]):
        super(MultiplayerCompetition, self).__init__(teams, name, game)
        assert issubclass(game, MultiPlayerGame)
        self.game = game(teams, name)

    @property
    def ranking(self) -> Dict[int, List]:

        scores = self.game.team_scores

        sort_idx = np.argsort(scores)[::-1]
        scores = np.array(scores)[sort_idx]
        teams = np.array(self.teams)[sort_idx]

        ranking: Dict[int, List] = {}
        prev = np.inf
        rank = 0
        for score, team in zip(scores, teams):
            if score < prev:
                rank += 1
            ranking[rank] = ranking.get(rank, []) + [team]
            prev = score
        return ranking

    def get_team_names(self) -> List[str]:
        return [team.name for team in self.teams]

    def __repr__(self) -> str:
        return f"Multiplayer Competition: '{self.name}'"

    @property
    def live_games(self) -> MultiPlayerGame:
        return self.game

    @property
    def winner(self) -> Optional[Team]:
        if self.ranking is None:
            return None
        if len(self.ranking[1]) != 1:
            raise NotImplementedError("Not dealt with multiple winners")
        return self.ranking[1][0]
