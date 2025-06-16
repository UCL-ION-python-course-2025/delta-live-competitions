from math import cos, radians, sin
from typing import List, Optional, Tuple

import pygame
import pygame.gfxdraw

from competition_controller import CompetitionController
from head_to_head_viewer import HeadToHeadGameViewer
from othello.game import OthelloGame

DISC_SIZE_RATIO = 0.8

BLUE_COLOR = (23, 93, 222)
BACKGROUND_COLOR = (0, 158, 47)
YELLOW_COLOR = (255, 240, 0)


BLACK_COLOR = (6, 9, 16)
GRAY_COLOR = (102, 102, 122)
WHITE_COLOR = (255, 255, 255)

TEAM_NAME_COLOR = BLACK_COLOR


class OthelloGameViewer(HeadToHeadGameViewer):
    GAME_HEIGHT = 6
    GAME_WIDTH = 6
    # Should probably be read from game.py
    N_ROWS = 6
    N_COLS = 6
    SQUARE_SIZE = 100
    FONT_SCALER = 13

    def __init__(self, controller: CompetitionController):
        super().__init__(controller)
        self.team_a_color = WHITE_COLOR
        self.team_b_color = BLACK_COLOR
        self.win_sequence: List[Optional[Tuple[int, int, int]]] = [None] * 3
        self.set_font()

    def reset_games(self) -> None:
        super().reset_games()
        self.set_font()
        self.SQUARE_SIZE = round(
            min(
                self.pixel_game_height / self.N_ROWS,
                self.pixel_game_width / self.N_COLS,
            )
        )

    def set_font(self) -> None:
        self._font = pygame.font.SysFont("arial", round(self.pixel_game_height / self.FONT_SCALER))

    def draw_win_message(self, game: OthelloGame) -> None:
        super().draw_win_message(
            game,
            position="middle",
            font_size_override=round(
                (self.pixel_game_height / self.FONT_SCALER) * 1.5
            ),  # Increase font size by 50%
        )

    def draw_round_win_message(self, game: OthelloGame, winner: Optional[int]) -> None:

        origin = self.get_game_origin(game)
        # game_height = self.SQUARE_SIZE * self.N_ROWS

        label_offset = self.pixel_game_width // 3
        game_height = self.SQUARE_SIZE * self.N_ROWS

        x_win_positions = [
            origin[0] - label_offset,
            origin[0] + game.cols * self.SQUARE_SIZE + label_offset,
        ]

        y_pos = origin[1] + game_height - self._font.get_height() * 2

        if winner is not None:
            self.create_text(
                text="Round Winner",
                color=YELLOW_COLOR,
                pos=(x_win_positions[winner != game.team_a], y_pos),
                font=self._font,
                max_width=self.pixel_game_width * 2 // 3,
                background_color=BLACK_COLOR,
            )

        else:
            for x_pos in x_win_positions:
                self.create_text(
                    text="Round Drawn",
                    color=YELLOW_COLOR,
                    pos=(x_pos, y_pos),
                    font=self._font,
                    max_width=self.pixel_game_width * 2 // 3,
                    background_color=BLACK_COLOR,
                )

    def draw_game(self, game: OthelloGame) -> None:
        """
        Draws board[c][r] with c = 0 and r = 0 being bottom left
        0 = empty (background color)
        1 = yellow
        -1 = red

        Args:
            game: The game to draw
        """
        origin = self.get_game_origin(game)

        if game.board_finished:
            self.draw_round_win_message(game, game.round_winner)

        # Label position either side of board
        label_offset = self.pixel_game_width // 3
        x_pos_lhs = origin[0] - label_offset
        x_pos_rhs = origin[0] + game.cols * self.SQUARE_SIZE + label_offset

        font_height = self._font.get_linesize()
        board_top = origin[1] + (font_height // 2) + self.SQUARE_SIZE

        disk_size = int(DISC_SIZE_RATIO * self.SQUARE_SIZE / 2)

        for name, bg_color, x_pos_labels, board_tile_count, total_tile_count in zip(
            [
                f"{game.team_a.name}",
                f"{game.team_b.name}",
            ],
            [self.team_a_color, self.team_b_color],
            [x_pos_lhs, x_pos_rhs],
            [game.tile_count[1], game.tile_count[-1]],
            [game.team_a_tile_count, game.team_b_tile_count],
        ):

            self.create_text(
                text=name,
                color=TEAM_NAME_COLOR,
                pos=(x_pos_labels, board_top),
                font=self._font,
                # max_width=
                background_color=None,
            )

            # Add the counter to the team name
            draw_counter(
                self._screen,
                x_pos_labels,
                board_top + self._font.get_height() + disk_size // 2,
                disk_size,
                outline_color=BLACK_COLOR,
                fill_color=bg_color,
            )

            img = self._font.render(
                f"Tiles on board: {board_tile_count}", True, TEAM_NAME_COLOR, None
            )
            rect = img.get_rect()
            rect.center = (
                x_pos_labels,
                board_top + font_height * 3,
            )
            self._screen.blit(img, rect)

            img = self._font.render(f"Total tiles: {total_tile_count}", True, TEAM_NAME_COLOR, None)
            rect = img.get_rect()
            rect.center = (x_pos_labels, origin[1] + self.SQUARE_SIZE * self.N_ROWS)
            self._screen.blit(img, rect)

        # Draw title
        title = game.name.split(": ")[0]
        img = self._font.render(title, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + (self.N_COLS * self.SQUARE_SIZE) // 2,
            origin[1] - self._font.get_height() // 2,
        )
        self._screen.blit(img, rect)

        # Draw the win sequence
        y_pos_win_sequence = (
            origin[1]
            + self.SQUARE_SIZE * self.N_ROWS
            + self._font.get_height() // 2
            + disk_size // 4  # Small margin to get the disc off the bottom of the board
        )

        text = self._font.render("Previous: ", True, BLACK_COLOR, None)
        rect = text.get_rect()
        text_x_pos = origin[0] + text.get_width()
        rect.center = (
            text_x_pos,
            y_pos_win_sequence,
        )
        self._screen.blit(text, rect)

        # Show results below
        results = (
            [result.outcome.value for result in game.team_a.results[-game.n_completed_games :]]
            if game.n_completed_games > 0
            else []
        )
        x_start_counter = text_x_pos + int(text.get_width() / 1.5)
        for idx in range(3):
            result = None if idx >= len(results) else results[idx]
            if result == 0:
                draw_yin_yang(
                    self._screen,
                    x_start_counter + (idx * disk_size * 2),
                    y_pos_win_sequence,
                    int(disk_size * 0.8),
                )
            else:
                color = (
                    GRAY_COLOR
                    if result is None
                    else game.team_a_color
                    if result == 1
                    else game.team_b_color
                )

                draw_counter(
                    self._screen,
                    x_start_counter + (idx * disk_size * 2),
                    y_pos_win_sequence,
                    int(disk_size * 0.8),
                    outline_color=BLACK_COLOR,
                    fill_color=color,
                )

        # Draw background of the board
        pygame.gfxdraw.box(
            self._screen,
            pygame.Rect(
                origin[0],
                origin[1],
                game.cols * self.SQUARE_SIZE,
                game.rows * self.SQUARE_SIZE,
            ),
            BACKGROUND_COLOR,
        )

        # Draw the lines on the board
        size = self.SQUARE_SIZE

        for x in range(self.N_ROWS):
            for y in range(self.N_COLS):
                pygame.gfxdraw.rectangle(
                    self._screen,
                    (origin[0] + x * size, origin[1] + y * size, size, size),
                    BLACK_COLOR,
                )

        # Draw the in play tiles
        for r in range(game.rows):
            for c in range(game.cols):

                space = game.board[r, c]

                color = (
                    self.team_a_color
                    if space == 1
                    else self.team_b_color
                    if space == -1
                    else BACKGROUND_COLOR
                )

                draw_counter(
                    self._screen,
                    origin[0] + c * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                    origin[1] + r * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                    disk_size,
                    fill_color=color,
                    outline_color=BACKGROUND_COLOR,
                )

    def get_rules(self) -> str:
        return (
            "\nEach round is a best-of-three games of Othello.\n\n"
            "The winner of a game is the player with the most tiles on the board at the end.\n\n"
            "Players can have an equal number of tiles at the end of the game, in which case the game is tied.\n\n"
            "The player who goes first in a game will alternate in the first two rounds.\n\n"
            "If one player wins both of the first two games, they are the round winner, otherwise a third game is played.\n\n"
            "In this third game, the player with the highest number of tiles across the first two games will go first.\n\n"
            "If the score is tied after three games, the player with the highest total number of tiles across all three games wins.\n\n"
            "If both the score and the total number of tiles are tied after three games, both teams progress.\n\n"
        )


def draw_counter(
    screen: pygame.Surface,
    x_pos: int,
    y_pos: int,
    size: int,
    outline_color: Tuple[int, int, int],
    fill_color: Optional[Tuple[int, int, int]],
) -> None:

    if fill_color is not None:
        pygame.gfxdraw.filled_circle(
            screen,
            x_pos,
            y_pos,
            size,
            fill_color,
        )

    pygame.gfxdraw.aacircle(
        screen,
        x_pos,
        y_pos,
        size,
        outline_color,
    )


def draw_yin_yang(screen: pygame.Surface, x_pos: int, y_pos: int, size: int) -> None:
    start_pos = 45
    pie(screen, BLACK_COLOR, (x_pos, y_pos), size, start_pos, start_pos + 180)
    pie(screen, WHITE_COLOR, (x_pos, y_pos), size, start_pos + 180, start_pos + 360)


def pie(
    screen: pygame.Surface,
    color: Tuple[int, int, int],
    center: Tuple[int, int],
    radius: int,
    start_angle: float,
    stop_angle: float,
) -> None:
    """Draw pie using parametric coordinates of circle."""
    theta = start_angle
    while theta <= stop_angle:
        pygame.draw.line(
            screen,
            color,
            center,
            (
                center[0] + radius * cos(radians(theta)),
                center[1] + radius * sin(radians(theta)),
            ),
            2,
        )
        theta += 0.01
