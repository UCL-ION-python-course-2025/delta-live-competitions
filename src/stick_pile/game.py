from typing import Tuple
from delta_stick_pile.game_mechanics import StickPile, choose_move_randomly
from game_parent import HeadToHeadGame, PlayState, PointsGame
from team import Team


BLACK_COLOR = (0, 0, 0)


class StickPileGame(HeadToHeadGame):
    """Inherit from PointsGame or HeadToHeadGame."""

    NAME = "StickPile"
    ROBOT_PLAYER = Team("Robot", choose_move_randomly)
    WIN_THRESHOLD = 3

    def __init__(self, team_a: Team, team_b: Team, name: str):
        self.team_a = team_a
        self.team_b = team_b
        self.team_a_color = BLACK_COLOR
        self.team_b_color = BLACK_COLOR
        self.env = StickPile(
            self.team_b.choose_move,
            verbose=False,
            render=False,  # Call render ourselves
            game_speed_multiplier=100000,
        )
        self.team_a_score = 0
        self.team_b_score = 0
        self.n_games = 0
        self.number_of_sticks_remaining = self.reset_game()
        self.name = name
        self.round_over = False
        self.doing_reset = False

        self.most_recent_move = None

    def reset_game(self) -> int:
        print("reset game called")
        self.invalid_move = False
        self.number_of_sticks_remaining, _, _, _ = self.env.reset(take_first_step=False)
        self.team_a_sticks_taken = 0
        self.team_b_sticks_taken = 0
        self.round_over = False
        super(StickPileGame, self).reset_game()

        return self.number_of_sticks_remaining

    def step(self) -> None:
        if self.completed:
            return

        if self.round_over:
            print("resetting")
            self.doing_reset = True
            self.reset_game()
            return

        self.doing_reset = False

        team_a_turn = self.env.player_move == "player"
        player_to_play = self.team_a if team_a_turn else self.team_b

        try:
            move = player_to_play.choose_move(
                number_of_sticks_remaining=self.env.number_of_sticks_remaining,
            )
        except:
            self.invalid_move = True
            move = None

        print(f"player to play {player_to_play.name}")
        if move is None:
            move = 0
        # This handles the player switch
        move_result = self.env._step(move)

        self.most_recent_move = move

        # Invalid move
        if move_result == -1:

            self.invalid_move = True
            print(
                f'{"team a" if team_a_turn else 'team_b'} made an invalid move and loses!'
            )
            if team_a_turn:
                self.team_b_score += 1
            else:
                self.team_a_score += 1

            self.round_over = True
            print([self.team_a_score, self.team_b_score])
            if self.WIN_THRESHOLD in [self.team_a_score, self.team_b_score]:
                self.play_state = PlayState.COMPLETED
            return

        if team_a_turn:
            self.team_a_sticks_taken += move
        else:
            self.team_b_sticks_taken += move

        self.number_of_sticks_remaining = self.env.number_of_sticks_remaining

        if move_result == 1:
            print(
                f"{self.team_a.name if team_a_turn else self.team_b.name} takes the last stick and wins!"
            )
            if team_a_turn:
                self.team_a_score += 1
            else:
                self.team_b_score += 1

            self.round_over = True
            print([self.team_a_score, self.team_b_score])
            if self.WIN_THRESHOLD in [self.team_a_score, self.team_b_score]:
                self.play_state = PlayState.COMPLETED
            return
