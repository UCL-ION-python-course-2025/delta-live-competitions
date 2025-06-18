import numpy as np

from competition_controller import wait_for_click
from delta_connect4.game_mechanics import (
    choose_move_randomly,
    get_empty_board,
    has_won,
    is_column_full,
    place_piece,
)
from game_parent import HeadToHeadGame
from team import Outcome, Result, Team


class Connect4Game(HeadToHeadGame):
    NAME = "Connect 4"
    ROBOT_PLAYER = Team("Robot", choose_move_randomly)

    def __init__(
        self,
        team_a: Team,
        team_b: Team,
        name: str,
        rows: int = 6,
        cols: int = 8,
    ) -> None:
        super().__init__(
            team_a,
            team_b,
            f"{name}: {team_a.name} vs {team_b.name}",
        )

        # Board dimensions
        self.rows = rows
        self.cols = cols

        self.num_games_played = 0

        self.player_turn = np.random.choice([-1, 1])
        self.went_first = self.player_turn
        self.reset_game()
        self.reset_me = False
        self.most_recent_column = None
        self.team_a_counter_to_win = None
        self.team_b_counter_to_win = None

    def reset_game(self) -> None:
        """Resets the game state (board and variables)"""
        self.board = get_empty_board(self.rows, self.cols)
        super().reset_game()
        # Alternate first turn .
        # (Gets flipped twice for the first game but oh well)
        self.player_turn = self.went_first * -1
        self.went_first = self.player_turn

    def step(self) -> None:
        # Only take a turn if the game is not over
        if self.winner is not None or self.completed:
            return

        if self.reset_me:
            wait_for_click()
            self.reset_me = False
            self.reset_game()
        # Get the right next player whose turn it is
        player = self.team_a if self.player_turn == 1 else self.team_b
        column_index = player.choose_move(board=self.player_turn * self.board)
        possible_moves = list(range(self.board.shape[1]))
        possible_moves = [
            move for move in possible_moves if not is_column_full(self.board, move)
        ]
        assert column_index in possible_moves
        self.board, row_idx = place_piece(self.board, column_index, self.player_turn)
        self.player_turn *= -1

        won = has_won(self.board, column_index)
        drawn = np.all(self.board != 0) and not won
        game_over = won or drawn

        self.most_recent_column = column_index  # For the visuals
        if not game_over:
            return

        self.num_games_played += 1
        self.store_results()

        if won:
            # team_a if the winner if the winning piece is 1.
            if self.board[row_idx, column_index] == 1:
                self.team_a_score += 1
                # Store number of counters it took team_a to win to act as tie-breaker
                self.team_a_counter_to_win = np.sum(self.board == 1)
            else:
                self.team_b_score += 1
                self.team_b_counter_to_win = np.sum(self.board == -1)

        if self.num_games_played < 2:
            self.reset_me = True
            return

        # Both games drawn
        if self.team_a_score == self.team_b_score == 0:
            self.both_teams_progress()
        # One game each
        elif self.team_a_score == self.team_b_score == 1:
            assert self.team_a_counter_to_win is not None
            assert self.team_b_counter_to_win is not None
            if self.team_a_counter_to_win < self.team_b_counter_to_win:
                # Add less than a whole point so it doesn't say "2-1" for a tiebreaker
                self.team_a_score += 0.1
            elif self.team_a_counter_to_win > self.team_b_counter_to_win:
                self.team_b_score += 0.1
            else:
                self.both_teams_progess()

        self.complete()

    def both_teams_progess(self) -> None:
        self.team_a_score += 1
        self.team_a.name = f"{self.team_a.name} & {self.team_b.name}"

    def store_results(self) -> None:
        """This may not be 100% reliable, untested."""
        self.team_a.results.append(
            Result(
                final_board=self.board.copy(),
                outcome=Outcome(
                    1
                    if self.winner == self.team_a
                    else -1 if self.winner == self.team_b else 0
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
                    if self.winner == self.team_b
                    else -1 if self.winner == self.team_a else 0
                ),
                match_name=self.name,
                opponent=self.team_a,
            )
        )
