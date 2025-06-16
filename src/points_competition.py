from typing import Dict, List, Optional, Type

import numpy as np

from competition import Competition
from game_parent import Game, PointsGame
from team import Team


class PointsCompetition(Competition):
    def __init__(self, teams: List[Team], name: str, game: Type[PointsGame]):
        super(PointsCompetition, self).__init__(teams, name, game)
        self.games = [game(name, team) for team in teams]

    @property
    def ranking(self) -> Dict[int, List]:

        # Only works for Wordle
        # scores = [game.n_rounds_solved * 100 - game.n_total_guesses for game in self.games]
        scores = [game.score for game in self.games]

        sort_idx = np.argsort(self.scores)[::-1]
        scores = np.array(self.scores)[sort_idx]
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

    def get_team_names(self) -> List[List[str]]:
        return self.teams[0].name

    @property
    def scores(self) -> List[int]:
        return [game.score for game in self.games]

    def __repr__(self) -> str:
        return f"Points-based Competition: '{self.name}'"

    @property
    def live_games(self) -> List[Game]:
        return self.games

    @property
    def winner(self) -> Optional[Team]:
        return self.ranking[1] if self.ranking is not None else None
