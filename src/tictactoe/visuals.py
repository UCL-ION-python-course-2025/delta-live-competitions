import math
from typing import Tuple

import pygame
import pygame.gfxdraw

from competition_controller import CompetitionController
from head_to_head_viewer import HeadToHeadGameViewer
from tictactoe.competitor_code.game_mechanics import (
    BG_COLOR,
    CIRCLE_RADIUS,
    CIRCLE_WIDTH,
    CROSS_WIDTH,
    HEIGHT,
    LINE_COLOR,
    LINE_WIDTH,
    SPACE,
    WIDTH,
    WIN_LINE_WIDTH,
    Cell,
)
from tictactoe.game import TictactoeGame

# colors
RED_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)


class TictactoeGameViewer(HeadToHeadGameViewer):
    CROSS_WIDTH = 25
    SPACE = 55
    GAME_WIDTH = WIDTH
    GAME_HEIGHT = HEIGHT

    def __init__(self, controller: CompetitionController):
        super().__init__(controller)
        self.game_origins = None
        self.pixel_game_width = 0
        self.pixel_game_height = 0
        self.square_size = 0

    def reset_games(self):
        super().reset_games()
        self.square_size = self.pixel_game_width // 3

    def game_coords_to_pixel_coords(self, game_coords: Tuple[int, int]) -> Tuple[int, int]:
        return round(game_coords[0] * self.game_to_pixel_ratio), round(
            game_coords[1] * self.game_to_pixel_ratio
        )

    def draw_game(self, game: TictactoeGame):
        """Draws match game on screen.

        Args:
            game: The game to draw
        """
        origin = self.get_game_origin(game)

        # Draw on title of the game on the left of it
        num_games = len(self.controller.rounds_of_games[-1])
        font = pygame.font.SysFont("monospace", 64 // round(math.sqrt(num_games)), bold=True)
        for count, (text, font_color, bg_color) in enumerate(
            zip(
                [game.team_a.name, "vs", game.team_b.name],
                [BLACK_COLOR, BLACK_COLOR, BLACK_COLOR],
                [game.team_a_color, None, game.team_b_color],
            )
        ):
            self.create_text(
                text=text,
                color=font_color,
                pos=(
                    origin[0] - self.pixel_game_width // 2,
                    origin[1]
                    + self.pixel_game_height // 2
                    + int((count - 1) * font.get_linesize() * 3),
                ),
                font=font,
                max_width=self.pixel_game_width * 2 // 3,
                background_color=bg_color,
            )

        # Draw the title
        title = game.name.split(": ")[0]
        img = self._font.render(title, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] - self._font.get_height() // 2 - 10,
        )
        self._screen.blit(img, rect)

        # Draw background of the board
        pygame.gfxdraw.box(
            self._screen,
            pygame.Rect(
                origin[0],
                origin[1],
                self.pixel_game_width,
                self.pixel_game_height,
            ),
            BG_COLOR,
        )

        # Draw both horizontal lines
        for line_num in range(1, 3):
            pygame.draw.line(
                self._screen,
                LINE_COLOR,
                (origin[0], origin[1] + self.square_size * line_num),
                (origin[0] + self.pixel_game_width, origin[1] + self.square_size * line_num),
                round(LINE_WIDTH * self.game_to_pixel_ratio),
            )

        # Draw both vertical lines
        for line_num in range(1, 3):
            pygame.draw.line(
                self._screen,
                LINE_COLOR,
                (origin[0] + line_num * self.square_size, origin[1]),
                (origin[0] + line_num * self.square_size, origin[1] + self.pixel_game_height),
                round(LINE_WIDTH * self.game_to_pixel_ratio),
            )

        # Draw circles and crosses based on board state
        for row in range(3):
            for col in range(3):
                if game.board[row][col] == Cell.O:
                    pygame.draw.circle(
                        self._screen,
                        game.team_b_color,
                        (
                            origin[0] + round(col * self.square_size + self.square_size // 2),
                            origin[1] + round(row * self.square_size + self.square_size // 2),
                        ),
                        round(CIRCLE_RADIUS * self.game_to_pixel_ratio),
                        round(CIRCLE_WIDTH * self.game_to_pixel_ratio),
                    )
                elif game.board[row][col] == Cell.X:
                    space_size = SPACE * self.game_to_pixel_ratio
                    pygame.draw.line(
                        self._screen,
                        game.team_a_color,
                        (
                            origin[0] + col * self.square_size + space_size,
                            origin[1] + row * self.square_size + self.square_size - space_size,
                        ),
                        (
                            origin[0] + col * self.square_size + self.square_size - space_size,
                            origin[1] + row * self.square_size + space_size,
                        ),
                        round(CROSS_WIDTH * self.game_to_pixel_ratio),
                    )
                    pygame.draw.line(
                        self._screen,
                        game.team_a_color,
                        (
                            origin[0] + col * self.square_size + space_size,
                            origin[1] + row * self.square_size + space_size,
                        ),
                        (
                            origin[0] + col * self.square_size + self.square_size - space_size,
                            origin[1] + row * self.square_size + self.square_size - space_size,
                        ),
                        round(CROSS_WIDTH * self.game_to_pixel_ratio),
                    )

        # Check for, and draw, win lines
        for player in [Cell.X, Cell.O]:
            for col in range(3):
                if (
                    game.board[0][col] == player
                    and game.board[1][col] == player
                    and game.board[2][col] == player
                ):
                    posX = origin[0] + col * self.square_size + self.square_size // 2

                    pygame.draw.line(
                        self._screen,
                        game.team_b_color if player == Cell.O else game.team_a_color,
                        (posX, origin[1] + 15),
                        (posX, origin[1] + self.pixel_game_height - 15),
                        round(WIN_LINE_WIDTH * self.game_to_pixel_ratio),
                    )

            for row in range(3):
                if (
                    game.board[row][0] == player
                    and game.board[row][1] == player
                    and game.board[row][2] == player
                ):
                    posY = origin[1] + row * self.square_size + self.square_size // 2

                    pygame.draw.line(
                        self._screen,
                        game.team_b_color if player == Cell.O else game.team_a_color,
                        (origin[0] + 15, posY),
                        (origin[0] + self.pixel_game_width - 15, posY),
                        round(WIN_LINE_WIDTH * self.game_to_pixel_ratio),
                    )

            if (
                game.board[2][0] == player
                and game.board[1][1] == player
                and game.board[0][2] == player
            ):
                pygame.draw.line(
                    self._screen,
                    game.team_b_color if player == Cell.O else game.team_a_color,
                    (origin[0] + 15, origin[1] + self.pixel_game_height - 15),
                    (origin[0] + self.pixel_game_width - 15, origin[1] + 15),
                    round(WIN_LINE_WIDTH * self.game_to_pixel_ratio),
                )

            if (
                game.board[0][0] == player
                and game.board[1][1] == player
                and game.board[2][2] == player
            ):
                pygame.draw.line(
                    self._screen,
                    game.team_b_color if player == Cell.O else game.team_a_color,
                    (origin[0] + 15, origin[1] + 15),
                    (
                        origin[0] + self.pixel_game_width - 15,
                        origin[1] + self.pixel_game_height - 15,
                    ),
                    round(WIN_LINE_WIDTH * self.game_to_pixel_ratio),
                )
