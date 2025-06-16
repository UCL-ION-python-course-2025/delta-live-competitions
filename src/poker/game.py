from typing import Tuple

from game_mechanics import PokerEnv, choose_move_randomly, wait_for_click
from game_parent import HeadToHeadGame, PlayState
from team import Outcome, Result, Team

BLACK_COLOR = (6, 9, 16)
WHITE_COLOR = (255, 255, 255)


class PokerGame(HeadToHeadGame):
    NAME = "Poker"
    ROBOT_PLAYER = Team("Robot", choose_move_randomly)

    def __init__(self, team_a: Team, team_b: Team, name: str):
        super().__init__(team_a, team_b, name)
        self.env = PokerEnv(
            self.team_b.choose_move,
            verbose=False,
            render=False,  # Call render ourselves
        )
        self.env.reset()
        self.team_a_score += self.env.STARTING_MONEY
        self.team_b_score += self.env.STARTING_MONEY
        self.n_games = 0
        self.env._toggle_reset_takes_step()

    def reset_game(self) -> Tuple[float, bool]:
        super(PokerGame, self).reset_game()
        _, reward, done, _ = self.env.reset()
        return reward, done

    def step(self) -> None:
        """Need to mimic the step() function of the env by calling _step and resetting here.

        This is to allow rendering after an immediate fold.
        """

        assert not self.env.reset_takes_step  # Sanity check

        if self.completed:
            return

        if self.env.hand_done and not self.env.done:
            wait_for_click()
            self.env.complete_hand()
            self.team_a_score: int = self.env.player_total
            self.team_b_score: int = self.env.opponent_total
            return

        if not self.env.done:

            if self.env.turn == 0:
                self.env._step(self.team_a.choose_move(state=self.env.player_state))
            elif self.env.turn == 1:
                self.env._step(self.team_b.choose_move(state=self.env.opponent_state))
            else:
                raise ValueError("Invalid turn")

        if self.env.done:
            self.play_state = PlayState.COMPLETED
            self.complete()
