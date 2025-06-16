from delta_pong.game_mechanics import PongEnv, robot_choose_move
from game_parent import HeadToHeadGame, PlayState
from team import Team


class PongGame(HeadToHeadGame):
    NAME = "Pong"
    ROBOT_PLAYER = Team("Robot", robot_choose_move)
    WIN_THRESHOLD = 25

    def __init__(
        self,
        team_a: Team,
        team_b: Team,
        name: str,
    ):
        HeadToHeadGame.__init__(
            self,
            team_a,
            team_b,
            name,
        )
        self.reset_game()

    def reset_game(self):
        super(PongGame, self).reset_game()
        self.env = PongEnv(self.team_b.choose_move)  # Really not sure about this

    def step(self) -> None:
        if self.completed:
            return
        self.env.step(self.team_a.choose_move(state=self.env.observation))
        if self.env.done:
            if self.env.ball.x <= 0:
                self.team_b_score += 1
            else:
                self.team_a_score += 1
            if self.team_a_score < self.WIN_THRESHOLD and self.team_b_score < self.WIN_THRESHOLD:
                self.reset_game()
            else:
                self.play_state = PlayState.COMPLETED
