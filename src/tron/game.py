from typing import Dict, List

from competition_controller import wait_for_click
from delta_tron.game_mechanics import BIKE_COLORS, TronEnv
from delta_tron.game_mechanics import rules_rollout as robot_choose_move
from game_parent import HeadToHeadGame, MultiPlayerGame, PlayState
from team import Team

# How many points you get per ranking
RANKING_TO_SCORE = {
    1: 1,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
}


class TronGame(HeadToHeadGame):
    NAME = "Tron"
    ROBOT_PLAYER = Team("Robot", robot_choose_move)
    WIN_THRESHOLD = 5

    def __init__(
        self,
        team_a: Team,
        team_b: Team,
        name: str,
    ):
        super().__init__(
            team_a, team_b, name, team_a_color=BIKE_COLORS[0], team_b_color=BIKE_COLORS[1]
        )

        # Choose the first team as the "team_a" so can use the game_mechanics env directly
        self.team_a = team_a
        self.team_b = team_b

        self.env = TronEnv(
            opponent_choose_move=self.team_b.choose_move,
            verbose=False,
            render=False,  # Call render ourselves
            game_speed_multiplier=100000,
        )

        self.env.reset()
        self.reset_game()

        # Map the names of the team here to the name of their bike in the env
        self.bike_names_map = {
            team.name: env_name for team, env_name in zip(self.teams, ["player", "opponent"])
        }

        if not self.is_robot_vs_robot_game:
            assert len(self.bike_names_map) == len(self.env.bikes)

        self.n_games = 0
        self.reset_me = False

    def reset_game(self) -> None:
        self.n_deaths = 0
        super(TronGame, self).reset_game()
        self.env.reset()
        self.game_ranking: Dict[str, int] = {}

    def step(self) -> None:
        if self.completed:
            return

        if self.env.done or self.reset_me:
            wait_for_click()
            self.reset_me = False
            self.reset_game()

        team_a_action = self.team_a.choose_move(state=self.env.state)
        _, reward, done, _ = self.env.step(team_a_action)

        if done:
            assert sum(bike.alive for bike in self.env.bikes) in [0, 1]
            if reward == 1:
                self.team_a_score += 1
            elif reward == -1:
                self.team_b_score += 1
            else:
                self.team_a_score += 1
                self.team_b_score += 1
            if any(score >= self.WIN_THRESHOLD for score in [self.team_a_score, self.team_b_score]):
                self.play_state = PlayState.COMPLETED
            else:
                self.reset_me = True
