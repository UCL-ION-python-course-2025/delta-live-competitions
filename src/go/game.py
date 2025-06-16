from typing import Tuple

from delta_go.game_mechanics import KOMI
from delta_go.game_mechanics import score as game_scorer
from game_mechanics import GoEnv, choose_move_randomly
from game_parent import HeadToHeadGame, PlayState
from team import Team

BLACK_COLOR = (6, 9, 16)
WHITE_COLOR = (255, 255, 255)


class GoGame(HeadToHeadGame):
    NAME = "Go"
    ROBOT_PLAYER = Team("Robot", choose_move_randomly)
    WIN_THRESHOLD = 1

    def __init__(self, team_a: Team, team_b: Team, name: str):
        super().__init__(team_a, team_b, name)
        self.env = GoEnv(
            self.team_b.choose_move,
            verbose=False,
            render=False,  # Call render ourselves
            game_speed_multiplier=100000,
        )

        self.team_a_score = 0
        self.team_b_score = 0
        self.n_games = 0
        self.team_a_color = BLACK_COLOR
        self.team_b_color = BLACK_COLOR

        # Allows us to take a step and so
        # display the score before resetting
        self.reset_me = False
        self.env.reset(player_black=True)

    def reset_game(self) -> Tuple[float, bool]:
        super(GoGame, self).reset_game()
        _, reward, done, _ = self.env.reset(player_black=True)
        self.reset_me = False
        return reward, done

    def step(self) -> None:
        if self.completed:
            return
        if self.reset_me:
            self.reset_game()

        team_a_turn = self.env.player_color == self.env.state.to_play

        player_to_play = self.team_a if team_a_turn else self.team_b

        move = player_to_play.choose_move(
            state=self.env.state,
        )

        self.env._step(move)
        self.most_recent_move = move
        done = self.env.done
        if done:
            self.n_games += 1
            black_score, white_score = game_scorer(
                self.env.state.board, KOMI, return_both_colors=True
            )
            team_a_is_black = self.env.player_color == 1
            if (
                team_a_is_black
                and black_score > white_score
                or not team_a_is_black
                and black_score < white_score
            ):
                self.team_a_score += 1
            else:
                self.team_b_score += 1

            if self.WIN_THRESHOLD in [self.team_a_score, self.team_b_score]:
                self.play_state = PlayState.COMPLETED
            self.reset_me = True

            # Reinit MCTS classes so trees do not persist across games
            if self.team_a.MctsClass is not None:
                self.team_a.mcts = self.team_a.MctsClass()

            if self.team_b.MctsClass is not None:
                self.team_b.mcts = self.team_b.MctsClass()
