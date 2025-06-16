from game_parent import PlayState, PointsGame
from team import Team
from twenty_forty_eight.competitor_code import TwentyFortyEight, robot_choose_move


class TwentyFortyEightGame(PointsGame, TwentyFortyEight):
    NAME = "2048"
    ROBOT_PLAYER = Team("Robot", robot_choose_move)

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
        TwentyFortyEight.__init__(self, competition=True)

    def step(self) -> None:
        if self.completed:
            return
        self.update(self._team.choose_move)
        if self.game_over:
            self.complete()
