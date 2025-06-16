from typing import List, Tuple

import numpy as np
import pygame
import pygame.gfxdraw

from competition_controller import CompetitionController
from connect4.game import Connect4Game
from delta_connect4.game_mechanics import get_top_piece_row_index, has_won
from head_to_head_viewer import HeadToHeadGameViewer

DISC_SIZE_RATIO = 0.8

BLUE_COLOR = (23, 93, 222)
BACKGROUND_COLOR = (19, 72, 162)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
LIGHT_GRAY_COLOR = (200, 200, 200)


class Connect4GameViewer(HeadToHeadGameViewer):
    GAME_HEIGHT = 6
    GAME_WIDTH = 8
    N_ROWS = 6
    N_COLS = 8
    SQUARE_SIZE = 100

    def __init__(self, controller: CompetitionController):
        super().__init__(controller)

    def reset_games(self):
        super().reset_games()
        self.SQUARE_SIZE = round(
            min(
                self.pixel_game_height / self.N_ROWS,
                self.pixel_game_width / self.N_COLS,
            )
        )

    def draw_game(self, game: Connect4Game):
        """
        Draws board[c][r] with c = 0 and r = 0 being bottom left
        0 = empty (background color)
        1 = yellow
        -1 = red

        Args:
            game: The game to draw
        """
        origin = self.get_game_origin(game)

        additional = (
            ""
            if game.team_a_counter_to_win is None
            else f"\n# To win: {game.team_a_counter_to_win}"
        )
        text_length = max(self._font.size(game.team_a.name)[0], self._font.size(additional)[0])
        self.create_text(
            text=game.team_a.name + additional,
            color=BLACK_COLOR,
            pos=(
                origin[0] - int(text_length / 2 * 1.1),
                origin[1] + self.pixel_game_height // 2,
            ),
            font=self._font,
            background_color=game.team_a_color,
        )

        additional = (
            ""
            if game.team_b_counter_to_win is None
            else f"\n# To win: {game.team_b_counter_to_win}"
        )
        text_length = max(self._font.size(game.team_b.name)[0], self._font.size(additional)[0])
        self.create_text(
            text=game.team_b.name + additional,
            color=BLACK_COLOR,
            pos=(
                origin[0] + self.pixel_game_width + int(text_length / 2 * 1.1),
                origin[1] + self.pixel_game_height // 2,
            ),
            font=self._font,
            background_color=game.team_b_color,
        )

        # Draw the score
        for count, (score, color) in enumerate(
            [(game.team_a_score, game.team_a_color), (game.team_b_score, game.team_b_color)]
        ):
            score = int(score)
            score_len = len(str(score))
            rect = pygame.Rect(
                origin[0]
                - self._font.get_height() * 5 * score_len // 4
                + count * (self.pixel_game_width + self._font.get_height() * 3 * score_len // 2),
                origin[1],
                self._font.get_height() * score_len,
                self._font.get_height() * 3 // 2,
            )
            pygame.draw.rect(self._screen, LIGHT_GRAY_COLOR, rect, 0, 3)
            pygame.draw.rect(self._screen, BLACK_COLOR, rect, 1, 3)

            img = self._font.render(str(score), True, color, LIGHT_GRAY_COLOR)
            rect = img.get_rect()
            rect.center = (
                origin[0]
                - self._font.get_height() * 3 * score_len // 4
                + count * (self.pixel_game_width + self._font.get_height() * 3 * score_len // 2),
                origin[1] + self._font.get_height() * 3 // 4,
            )
            self._screen.blit(img, rect)

        title = game.name.split(": ")[0]
        img = self._font.render(title, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + (self.N_COLS * self.SQUARE_SIZE) // 2,
            origin[1] - self._font.get_height() // 2 - 10,
        )
        self._screen.blit(img, rect)

        # Draw background of the board
        pygame.gfxdraw.box(
            self._screen,
            pygame.Rect(
                origin[0],
                origin[1],
                game.cols * self.SQUARE_SIZE,
                game.rows * self.SQUARE_SIZE,
            ),
            BLUE_COLOR,
        )

        if game.most_recent_column is None:
            winner = None
        elif has_won(game.board, game.most_recent_column):
            top = get_top_piece_row_index(game.board, game.most_recent_column)
            winner = game.board[top, game.most_recent_column]
            winning_pieces = get_pieces_four_connected(game.board, (top, game.most_recent_column))
        else:
            winner = None

        # Draw the circles - either as spaces if filled or
        for r in range(game.rows):
            for c in range(game.cols):
                space = game.board[r, c]
                color = (
                    game.team_a_color
                    if space == 1
                    else game.team_b_color
                    if space == -1
                    else BACKGROUND_COLOR
                )

                disc_size = int(DISC_SIZE_RATIO * self.SQUARE_SIZE / 2)

                if winner is not None and winner == space and (r, c) in winning_pieces:
                    pygame.gfxdraw.filled_circle(
                        self._screen,
                        origin[0] + c * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                        origin[1] + r * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                        int(disc_size * 1.35),
                        WHITE_COLOR,
                    )

                # Anti-aliased circle drawing
                pygame.gfxdraw.aacircle(
                    self._screen,
                    origin[0] + c * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                    origin[1] + r * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                    disc_size,
                    color,
                )

                pygame.gfxdraw.filled_circle(
                    self._screen,
                    origin[0] + c * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                    origin[1] + r * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                    disc_size,
                    color,
                )

    def get_rules(self) -> str:
        return (
            "Each round consists of two games of connect4\n\n"
            "Each player will take the first turn in one of the games\n\n"
            "If a player wins both games they are declared the winner\n\n"
            "In the event of a tie, the player who won their game in the least number of moves wins\n\n"
            "If the number of moves is the same, both teams progress\n\n"
        )


def get_pieces_four_connected(
    board: np.ndarray, piece_location: Tuple[int, int]
) -> List[Tuple[int, int]]:
    """Adapted from game_mechanics, gets the location of 4 connected pieces. Only call this if you
    know there is a winner.

    Args:
        board: The board to check
        piece_location: The location of the piece to check (row, col)

    Returns: List of (row, col) tuples of the pieces that are four connected
    """
    player = board[piece_location]
    directions = [
        [0, 1],
        [1, 1],
        [1, 0],
        [1, -1],
    ]

    # Try all directions
    for direction in directions:
        connected_four = [piece_location]

        # We're looking for the longest line through this piece,
        #  start at the piece with a line of 1
        num_in_a_row = 1

        # Try spaces in positive direction
        steps_in_positive_dir = 1

        # Take steps in positive direction until we hit a space not filled by this player's piece
        row = piece_location[0] + steps_in_positive_dir * direction[0]
        col = piece_location[1] + steps_in_positive_dir * direction[1]
        while 0 <= row < board.shape[0] and 0 <= col < board.shape[1] and board[row, col] == player:
            connected_four.append((row, col))
            num_in_a_row += 1
            steps_in_positive_dir += 1
            row = piece_location[0] + steps_in_positive_dir * direction[0]
            col = piece_location[1] + steps_in_positive_dir * direction[1]

        # Try spaces in negative direction
        steps_in_negative_dir = 1

        row = piece_location[0] - steps_in_negative_dir * direction[0]
        col = piece_location[1] - steps_in_negative_dir * direction[1]

        while (
            row in range(board.shape[0])
            and col in range(board.shape[1])
            and board[row, col] == player
        ):
            connected_four.append((row, col))
            num_in_a_row += 1
            steps_in_negative_dir += 1
            row = piece_location[0] - steps_in_negative_dir * direction[0]
            col = piece_location[1] - steps_in_negative_dir * direction[1]
        if len(connected_four) >= 4:
            return connected_four

    raise ValueError("No four connected pieces found")
