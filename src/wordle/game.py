import numpy as np

from game_parent import PlayState, PointsGame
from team import Team
from wordle.competitor_code import Wordle, robot_choose_move


class WordleGame(PointsGame, Wordle):
    NAME = "wordle"
    ROBOT_PLAYER = Team("Robot", robot_choose_move)
    WIN_THRESHOLD = 5
    GAME_SPEED_MULTIPLIER = 100

    def __init__(
        self,
        name: str,
        team: Team,
    ):
        PointsGame.__init__(
            self,
            name,
            team,
        )
        self.seed = 42
        np.random.seed(self.seed)
        self.n_rounds = 0
        Wordle.__init__(self, team.name, WordleGame.GAME_SPEED_MULTIPLIER)
        self.n_total_guesses = 0
        self.total_rounds = 6
        self.n_rounds_solved = 0
        self.score = 100
        self.timeout = 2

    def step(self) -> None:

        if self.completed:
            return
        self.update(self._team.choose_move)
        self.score -= 100

        if self.game_over or self.solved:
            self.n_rounds += 1
            if self.solved:
                self.n_rounds_solved += 1
            self.n_total_guesses += self.n_guesses
            self.complete()

        return
