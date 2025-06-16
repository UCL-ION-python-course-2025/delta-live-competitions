from game_parent import PlayState, PointsGame
from snake.competitor_code import Snake, robot_choose_move
from team import Team


class SnakeGame(PointsGame, Snake):
    NAME = "Snake"
    ROBOT_PLAYER = Team("Robot", robot_choose_move)
    MAX_STEPS = 10000

    def __init__(
        self,
        name: str,
        team: Team,
    ):
        PointsGame.__init__(self, name, team)
        Snake.__init__(self)

    def step(self) -> None:
        if self.completed:
            return
        print(self._team.name, "is playing...")
        self.update(self._team.choose_move)
        self.score = self.snake_length - 2
        if not self.snake_alive or self.steps_remaining == 0:
            self.play_state = PlayState.COMPLETED

    @property
    def steps_remaining(self) -> int:
        return self.MAX_STEPS - self.num_steps_taken
