import random
from dataclasses import dataclass

from game_parent import HeadToHeadGame
from team import Team
from tictactoe.competitor_code import team4_choose_move
from tictactoe.competitor_code.game_mechanics import (
    Cell,
    TictactoeMechanics,
    convert_to_indices,
    flatten_board,
)


@dataclass
class Turn:
    row: int
    column: int


class TictactoeGame(HeadToHeadGame, TictactoeMechanics):
    NAME = "Tictactoe"
    ROBOT_PLAYER = Team("Robot", team4_choose_move)

    def __init__(
        self,
        team_a: Team,
        team_b: Team,
        name: str,
        is_friendly: bool = False,
    ):
        HeadToHeadGame.__init__(
            self,
            team_a,
            team_b,
            name,
            is_friendly,
        )
        TictactoeMechanics.__init__(self)
        self.cell_to_team = {Cell.X: team_a, Cell.O: team_b}

    def reset_game(self):
        super(TictactoeGame, self).reset_game()
        self.restart()

    def step(self) -> None:
        if self.completed:
            return
        if self.is_game_over() and self.winner is None:
            self.reset_game()
            return
        flat_board = flatten_board(self.board)
        move = self.next_to_play.choose_move(flat_board)
        poss_move_list = poss_moves(flat_board)
        if move not in poss_move_list:
            print(
                f"{self.next_to_play.name} failed to play a move! Their move was: {move}"
            )
            move = random.choice(poss_move_list)
        move_tuple = convert_to_indices(move)
        piece = Cell.X if self.next_to_play == self.team_a else Cell.O
        self.update(move_tuple, piece)
        self.player_turn *= -1

        if self.is_game_over() and any(
            score != 0 for score in [self.team_a_score, self.team_b_score]
        ):
            self.complete()

    def is_game_over(self) -> bool:
        winner = self._check_winner()

        if winner is not None:
            if self.cell_to_team[winner] == self.team_a:
                self.team_a_score += 1
            else:
                self.team_b_score += 1
            return True

        is_draw = self.is_board_full()
        if is_draw:
            return is_draw

        return False


def poss_moves(board):
    return [count for count, square in enumerate(board) if square == 0]
