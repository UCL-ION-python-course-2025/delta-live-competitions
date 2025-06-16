import math
from typing import Dict, List, Tuple

import pygame
import pygame.gfxdraw

from competition_controller import CompetitionController
from delta_wild_tictactoe.game_mechanics import (
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
from head_to_head_viewer import HeadToHeadGameViewer

from .game import WildTictactoeGame

# colors
COLOR = Tuple[int, int, int]
RED_COLOR: COLOR = (255, 0, 0)
BLACK_COLOR: COLOR = (26, 28, 31)
WHITE_COLOR: COLOR = (255, 255, 255)


def flatten_board(board: List[List[Cell]]) -> List[Cell]:
    return [x for xs in board for x in xs]


class WildTictactoeGameViewer(HeadToHeadGameViewer):
    CROSS_WIDTH = 25
    SPACE = 55
    GAME_WIDTH = WIDTH
    GAME_HEIGHT = HEIGHT

    def __init__(self, controller: CompetitionController):
        self.pixel_game_width = 0
        self.pixel_game_height = 0
        self.square_size = 0
        super().__init__(controller)
        # Below is {game_number: {(row, col): (R, G, B)}}
        self.counter_colors: Dict[int, Dict[Tuple[int, int], COLOR]] = {}

    def reset_games(self) -> None:
        super().reset_games()
        self.square_size = self.pixel_game_width // 3
        self.counter_colors = {}

    def game_coords_to_pixel_coords(
        self, game_coords: Tuple[int, int]
    ) -> Tuple[int, int]:
        return round(game_coords[0] * self.game_to_pixel_ratio), round(
            game_coords[1] * self.game_to_pixel_ratio
        )

    def draw_title(self, title: str):
        # Write title at the top
        title_font = pygame.font.SysFont("arial", 64)
        screen_width, _ = pygame.display.get_surface().get_size()
        self.create_text(
            # self.competition.name,
            title,
            BLACK_COLOR,
            pos=(screen_width // 2, title_font.get_linesize()),
            font=title_font,
        )

    def draw_game(self, game: WildTictactoeGame) -> None:
        """Draws match game on screen.

        Args:
            game: The game to draw
        """
        game_num = self.games.index(game)
        # Reset the dictionary keeping track of which color is which
        if flatten_board(game.board).count(Cell.EMPTY) == 9:
            self.counter_colors[game_num] = {}

        origin = self.get_game_origin(game)

        # Draw the title - if only 1 competition involved in live games, put title at top
        #  otherwise put it above each game
        if (
            len(
                [
                    comp
                    for comp in self.controller.competitions
                    for g in self.games
                    if g in comp.live_games
                ]
            )
            == 1
        ):
            self.draw_title(game.name.split(": ")[0])
        else:
            title = game.name.split(": ")[0]
            img = self._font.render(title, True, BLACK_COLOR, None)
            rect = img.get_rect()
            rect.center = (
                origin[0] + self.pixel_game_width // 2,
                origin[1] - self._font.get_height() // 2 - 10,
            )
            self._screen.blit(img, rect)

        # Draw on title of the game on the left of it
        num_games = len(self.controller.rounds_of_games[-1])
        font = pygame.font.SysFont(
            "monospace", int(40 / num_games ** (1 / 3)), bold=True
        )
        for count, (text, font_color, bg_color) in enumerate(
            zip(
                [
                    f"{game.team_a.name} Score: {game.team_a_score} ",
                    "vs",
                    f"{game.team_b.name} Score: {game.team_b_score}",
                ],
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
                (
                    origin[0] + self.pixel_game_width,
                    origin[1] + self.square_size * line_num,
                ),
                round(LINE_WIDTH * self.game_to_pixel_ratio),
            )

        # Draw both vertical lines
        for line_num in range(1, 3):
            pygame.draw.line(
                self._screen,
                LINE_COLOR,
                (origin[0] + line_num * self.square_size, origin[1]),
                (
                    origin[0] + line_num * self.square_size,
                    origin[1] + self.pixel_game_height,
                ),
                round(LINE_WIDTH * self.game_to_pixel_ratio),
            )

        # Draw circles and crosses based on board state
        if game.robot_first_move:
            team_color = WHITE_COLOR
        # Need to flip this as visualisation is called after step() which
        # switches the player's turn
        elif game.next_to_play == game.team_b:
            team_color = game.team_a_color
        else:
            team_color = game.team_b_color

        nested_board = [game.board[i : i + 3] for i in range(0, len(game.board), 3)]
        for row in range(3):
            for col in range(3):
                color = self.counter_colors[game_num].get((row, col), team_color)
                if nested_board[row][col] == Cell.O:
                    self.counter_colors[game_num][(row, col)] = color
                    pygame.draw.circle(
                        self._screen,
                        color,
                        (
                            origin[0]
                            + round(col * self.square_size + self.square_size // 2),
                            origin[1]
                            + round(row * self.square_size + self.square_size // 2),
                        ),
                        round(CIRCLE_RADIUS * self.game_to_pixel_ratio),
                        round(CIRCLE_WIDTH * self.game_to_pixel_ratio),
                    )
                elif nested_board[row][col] == Cell.X:
                    # color = self.counter_colors.get((row, col), color)
                    self.counter_colors[game_num][(row, col)] = color
                    space_size = SPACE * self.game_to_pixel_ratio
                    pygame.draw.line(
                        self._screen,
                        color,
                        (
                            origin[0] + col * self.square_size + space_size,
                            origin[1]
                            + row * self.square_size
                            + self.square_size
                            - space_size,
                        ),
                        (
                            origin[0]
                            + col * self.square_size
                            + self.square_size
                            - space_size,
                            origin[1] + row * self.square_size + space_size,
                        ),
                        round(CROSS_WIDTH * self.game_to_pixel_ratio),
                    )
                    pygame.draw.line(
                        self._screen,
                        color,
                        (
                            origin[0] + col * self.square_size + space_size,
                            origin[1] + row * self.square_size + space_size,
                        ),
                        (
                            origin[0]
                            + col * self.square_size
                            + self.square_size
                            - space_size,
                            origin[1]
                            + row * self.square_size
                            + self.square_size
                            - space_size,
                        ),
                        round(CROSS_WIDTH * self.game_to_pixel_ratio),
                    )

        # Check for, and draw, win lines
        for player in [Cell.X, Cell.O]:
            for col in range(3):
                if (
                    nested_board[0][col] == player
                    and nested_board[1][col] == player
                    and nested_board[2][col] == player
                ):
                    posX = origin[0] + col * self.square_size + self.square_size // 2

                    pygame.draw.line(
                        self._screen,
                        # game.team_b_color if player == Cell.O else game.team_a_color,
                        team_color,
                        (posX, origin[1] + 15),
                        (posX, origin[1] + self.pixel_game_height - 15),
                        round(WIN_LINE_WIDTH * self.game_to_pixel_ratio),
                    )

            for row in range(3):
                if (
                    nested_board[row][0] == player
                    and nested_board[row][1] == player
                    and nested_board[row][2] == player
                ):
                    posY = origin[1] + row * self.square_size + self.square_size // 2

                    pygame.draw.line(
                        self._screen,
                        # game.team_b_color if player == Cell.O else game.team_a_color,
                        team_color,
                        (origin[0] + 15, posY),
                        (origin[0] + self.pixel_game_width - 15, posY),
                        round(WIN_LINE_WIDTH * self.game_to_pixel_ratio),
                    )

            if (
                nested_board[2][0] == player
                and nested_board[1][1] == player
                and nested_board[0][2] == player
            ):
                pygame.draw.line(
                    self._screen,
                    # game.team_b_color if player == Cell.O else game.team_a_color,
                    team_color,
                    (origin[0] + 15, origin[1] + self.pixel_game_height - 15),
                    (origin[0] + self.pixel_game_width - 15, origin[1] + 15),
                    round(WIN_LINE_WIDTH * self.game_to_pixel_ratio),
                )

            if (
                nested_board[0][0] == player
                and nested_board[1][1] == player
                and nested_board[2][2] == player
            ):
                pygame.draw.line(
                    self._screen,
                    # game.team_b_color if player == Cell.O else game.team_a_color,
                    team_color,
                    (origin[0] + 15, origin[1] + 15),
                    (
                        origin[0] + self.pixel_game_width - 15,
                        origin[1] + self.pixel_game_height - 15,
                    ),
                    round(WIN_LINE_WIDTH * self.game_to_pixel_ratio),
                )
