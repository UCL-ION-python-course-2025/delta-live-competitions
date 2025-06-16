import time

from delta_shooter.game_mechanics import ShooterEnv, choose_move_randomly
from game_parent import HeadToHeadGame, PlayState
from team import Team

PLAYER_ONE_COLOR = (171, 0, 215)
PLAYER_TWO_COLOR = (196, 0, 0)


class ShooterGame(HeadToHeadGame):
    NAME = "Shooter"
    ROBOT_PLAYER = Team("Robot", choose_move_randomly)
    # Adjust these constants down if the bots suck!!
    WIN_THRESHOLD = 10
    MAX_TIME = 60

    def __init__(self, team_a: Team, team_b: Team, name: str):
        # Set colours relating to the two sprites below - currently red and yellow
        super().__init__(
            team_a,
            team_b,
            name,
            team_a_color=PLAYER_ONE_COLOR,
            team_b_color=PLAYER_TWO_COLOR,
            both_teams_progress_on_draw=True,
        )
        self.env = ShooterEnv(self.team_b.choose_move, False)
        self.both_teams_progress_on_draw = True
        self.timer_started = False
        self.time_elapsed = 0.0

    def reset_game(self) -> None:
        super(ShooterGame, self).reset_game()
        self.env.reset()
        self.timer_started = False
        self.time_elapsed = 0.0

    def step(self) -> None:
        if not self.timer_started:
            self.start_time = time.time()
            self.timer_started = True

        self.time_elapsed = time.time() - self.start_time

        if self.completed:
            return

        move = self.team_a.choose_move(state=self.env.observation_player1)
        _, reward, done, _ = self.env.step(int(move))

        if not done and self.time_elapsed < self.MAX_TIME:
            return

        if reward == -1:
            self.team_b_score += 1
        elif reward == 1:
            self.team_a_score += 1
        else:  # A draw - Resevoir Dogs style. Or timeout
            self.team_a_score += 1
            self.team_b_score += 1

        if self.team_a_score < self.WIN_THRESHOLD and self.team_b_score < self.WIN_THRESHOLD:
            self.reset_game()
        else:
            self.play_state = PlayState.COMPLETED
            self.complete()
