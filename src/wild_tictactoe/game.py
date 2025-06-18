import random
from dataclasses import dataclass
from typing import List, Optional, Tuple

from delta_wild_tictactoe.game_mechanics import Cell, WildTictactoeEnv
from delta_wild_tictactoe.game_mechanics import (
    choose_move_randomly as robot_choose_move,
)
from delta_wild_tictactoe.game_mechanics import (
    get_empty_board,
    is_board_full,
    is_winner,
    place_counter,
)
from game_parent import HeadToHeadGame
from team import Team

TEAM_A_COLOR = (245, 66, 96)
TEAM_B_COLOR = (16, 181, 227)


@dataclass
class Turn:
    row: int
    column: int


class WildTictactoeGame(HeadToHeadGame):
    NAME = "Wild Tictactoe"
    ROBOT_PLAYER = Team("Robot", robot_choose_move)

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
            TEAM_A_COLOR,
            TEAM_B_COLOR,
            both_teams_progress_on_draw=True,
        )
        WildTictactoeEnv.__init__(self)
        self.game_over = False
        self.n_consec_draws = 0
        self.n_games_round = 0
        self.robot_first_move = False
        self.robot_first_move_location: Optional[Tuple] = None
        self.board = get_empty_board()

    def reset_game(self) -> None:
        self.player_turn = int(self.went_first) * -1
        self.went_first: int = self.player_turn
        super(WildTictactoeGame, self).reset_game()
        self.game_over = False
        self.board = get_empty_board()

    def step(self) -> None:
        if self.completed:
            return

        # The round continues with another game as no
        # overall winner yet.
        if self.game_over and self.winner is None:
            self.reset_game()
            return

        # Random first tile if there's no conclusive winner after 2 games.
        if self.board.count(" ") == 9 and self.n_games_round >= 2:
            # We switch turn order because a move is always taken at random at the start.
            # This way the player who plays first alternates in the same order:
            # I.e. if team A goes first in game 1, they go first in game 3, 5, 7 etc.
            self.player_turn *= -1

            if self.robot_first_move_location is None:
                move, counter = robot_choose_move(self.board.copy())
                self.robot_first_move_location = (move, counter)
            else:
                # Alternate between picking randomly and using the last randomly-picked move.
                # This ensures both players start with boards with the identical random move taken.
                move, counter = self.robot_first_move_location
                self.robot_first_move_location = None
            self.robot_first_move = True
        else:
            try:
                move, counter = self.next_to_play.choose_move(board=self.board.copy())
            except Exception as e:
                print(
                    f"Invalid move from {self.next_to_play.name} choosing move randomly"
                )
                move, counter = robot_choose_move(board=self.board.copy())

            self.robot_first_move = False

        poss_move_list = poss_moves(self.board)
        if move not in poss_move_list:
            raise ValueError(
                f"{self.next_to_play.name} failed to play a move! Their move was: {move}, possible moves: {poss_move_list}"
            )

        self.board = place_counter(self.board, move, counter)
        self.game_over = self.is_game_over()

        if self.game_over:
            if self.is_draw():
                self.n_consec_draws += 1
            else:
                self.n_consec_draws = 0
            if (
                abs(self.team_a_score - self.team_b_score) == 2
                or self.team_a_score == 6
                or self.team_b_score == 6
                or self.n_consec_draws == 6
            ):
                self.complete()
            else:
                self.n_games_round += 1

        # Very important and sacred.
        # Switches the turn, make sure everything else in the function
        # happens before this.
        self.player_turn *= -1

    def check_win(self) -> bool:
        if is_winner(self.board):
            if self.next_to_play == self.team_a:
                self.team_a_score += 1
            else:
                self.team_b_score += 1
            return True
        return False

    def is_draw(self) -> bool:
        return is_board_full(self.board)

    def is_game_over(self) -> bool:
        return self.check_win() or self.is_draw()


def poss_moves(board) -> List[int]:
    return [count for count, square in enumerate(board) if square == Cell.EMPTY]
