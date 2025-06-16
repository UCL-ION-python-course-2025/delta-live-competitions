from typing import Dict

import numpy as np

from competition_controller import wait_for_click
from game_mechanics import (
    choose_move_randomly,
    get_empty_board,
    get_legal_moves,
    has_legal_move,
    make_move,
)
from game_parent import HeadToHeadGame
from team import Outcome, Result, Team

BLACK_COLOR = (6, 9, 16)
WHITE_COLOR = (255, 255, 255)


class OthelloGame(HeadToHeadGame):
    NAME = "Othello Game"
    ROBOT_PLAYER = Team("Robot", choose_move_randomly)

    def __init__(
        self,
        team_a: Team,
        team_b: Team,
        name: str,
        rows: int = 6,
        cols: int = 6,
    ) -> None:
        super().__init__(
            team_a,
            team_b,
            f"{name}: {team_a.name} vs {team_b.name}",
            WHITE_COLOR,
            BLACK_COLOR,
        )

        # Board dimensions
        self.rows = rows
        self.cols = cols

        self.n_consec_draws = 0
        self.n_completed_games = 0
        self.player_turn = np.random.choice([-1, 1])
        self.went_first = self.player_turn
        self.team_a_tile_count = 2
        self.team_b_tile_count = 2

        # Store count from previous games
        self.team_a_previous_count = 0
        self.team_b_previous_count = 0

        self.reset_game()

    def reset_game(self) -> None:
        """Resets the game state (board and variables)"""

        super().reset_game()
        # Alternate first turn for game 1 and 2. Then player
        # with most tiles go first
        # Gets flipped twice for the first game but oh well

        self.board_finished = False
        if self.n_completed_games < 2:
            self.player_turn = self.went_first * -1
            self.went_first = self.player_turn
        else:
            self.player_turn = (
                1 if self.team_a_tile_count > self.team_b_tile_count else -1
            )

        self.board = get_empty_board(board_dim=self.rows, player_start=self.player_turn)

    def step(self) -> None:

        # Take an extra step if the board is finished so
        # can draw the end of the board message
        if self.board_finished:
            wait_for_click()
            self.reset_game()

        # Only take a turn if the game is not over
        if self.winner is not None and (not self.completed or not self.is_friendly):
            return
        # Get the right next player whose turn it is
        player = self.team_a if self.player_turn == 1 else self.team_b
        move = player.choose_move(state=self.player_turn * self.board)
        if possible_moves := get_legal_moves(self.player_turn * self.board):
            assert move in possible_moves

        else:
            assert move is None
        # Suboptimal double board flip
        if move is not None:
            self.board = (
                make_move(self.board * self.player_turn, move) * self.player_turn
            )
        self.player_turn *= -1

        self.team_a_tile_count = self.tile_count[1] + self.team_a_previous_count
        self.team_b_tile_count = self.tile_count[-1] + self.team_b_previous_count

        if not self.game_over:
            return

        self.board_finished = True
        self.n_completed_games += 1
        if self.tile_count[1] > self.tile_count[-1]:
            self.team_a_score += 1
            self.round_winner = self.team_a
        elif self.tile_count[1] < self.tile_count[-1]:
            self.round_winner = self.team_b
            self.team_b_score += 1
        else:
            self.round_winner = None
            self.team_a_score += 0.5
            self.team_b_score += 0.5

        self.team_a_previous_count += self.tile_count[1]
        self.team_b_previous_count += self.tile_count[-1]

        self.store_results()

        round_winner = (
            abs(self.team_a_score - self.team_b_score) == 2
            or self.n_completed_games == 3
        )

        if not round_winner:  # Reset done on next function call
            return

        if self.team_a_score == self.team_b_score and self.n_completed_games == 3:
            # If equal score, most tiles wins
            if self.team_a_tile_count > self.team_b_tile_count:
                self.team_a_score += 1
            elif self.team_a_tile_count < self.team_b_tile_count:
                self.team_b_score += 1
            else:
                # Stops infinite draws. If you get two draws both teams progress
                # with team_a representing.
                self.team_a_score += 1
                self.team_a.name = f"{self.team_a.name} & {self.team_b.name}"

        self.complete()

    @property
    def tile_count(self) -> Dict:
        return {1: np.sum(self.board == 1), -1: np.sum(self.board == -1)}

    @property
    def game_over(self) -> bool:
        return (
            not has_legal_move(self.board, self.player_turn)
            and not has_legal_move(self.board, self.player_turn * -1)
            or np.sum(self.board != 0) == self.board.shape[0] ** 2
        )

    def store_results(self) -> None:
        self.team_a.results.append(
            Result(
                final_board=self.board.copy(),
                outcome=Outcome(
                    1
                    if self.round_winner == self.team_a
                    else -1 if self.round_winner == self.team_b else 0
                ),
                match_name=self.name,
                opponent=self.team_b,
            )
        )
        self.team_b.results.append(
            Result(
                final_board=self.board.copy(),
                outcome=Outcome(
                    1
                    if self.round_winner == self.team_b
                    else -1 if self.round_winner == self.team_a else 0
                ),
                match_name=self.name,
                opponent=self.team_a,
            )
        )
