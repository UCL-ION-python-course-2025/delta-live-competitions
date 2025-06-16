import math
from typing import Dict, Tuple

import pygame
import pygame.gfxdraw

from competition_controller import CompetitionController
from observation import Observer
from pathfinder import PathfinderGame

BLUE_COLOR = (23, 93, 222)
YELLOW_COLOR = (255, 240, 0)
RED_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (19, 72, 162)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)


class PathfinderGameViewer(Observer):
    def __init__(self, controller: CompetitionController):
        super().__init__(controller)
        # Hard-coded. Fight me
        self.n_rows = 10
        self.n_cols = 10

        self.board_origins = None

    def reset_games(self):
        game_rows, game_cols = self.get_game_rows_cols()

        margin_size = 80  # pixels

        board_row_height = self._screen.get_height() / (game_rows + 1)
        board_col_width = self._screen.get_width() / (game_cols * 1.5)
        max_square_size = 100

        self.square_size = round(
            min(
                max_square_size,
                (board_row_height - margin_size) / self.n_rows,
                (board_col_width - (2 * margin_size)) / self.n_cols,
            )
        )
        self.board_origins = self.get_origins(
            (self.square_size * self.n_cols, self.square_size * self.n_rows)
        )
        self._font = pygame.font.SysFont("arial", round(self.square_size * 8 / 5))
        self.draw_all_games()
        # self.draw_knockout_tournament_tree(self.controller.competitions[0])

    def get_game_rows_cols(self):
        n_games = len(self.games)
        game_cols = 4 if n_games >= 10 else 3 if n_games >= 5 else 2 if n_games >= 3 else 1
        game_rows = math.ceil(len(self.games) / game_cols)
        return game_rows, game_cols

    def get_game_origin(self, game: PathfinderGame) -> Tuple[int, int]:
        assert self.board_origins is not None
        return self.board_origins[self.games.index(game)]

    def get_origins(self, game_dims: Tuple[float, float]) -> Dict[int, Tuple[int, int]]:
        # Figure out the number of columns and rows of games
        game_rows, game_cols = self.get_game_rows_cols()

        board_row_height = self._screen.get_height() / (game_rows + 1)
        board_col_width = self._screen.get_width() / (game_cols * 2)

        origins = {}
        for count, game in enumerate(self.games):
            x_origin = board_col_width - game_dims[0] / 2
            x_origin += (
                (count % game_cols) * 2 * board_col_width
            )  # If 2 rows: if odd - right col. If even - left col
            y_origin = board_row_height - game_dims[1] / 2
            y_origin += (
                count // game_cols
            ) * board_row_height  # If odd, bottom row, if even, top row
            origins[count] = (round(x_origin), round(y_origin))

        return origins

    def draw_game(self, game: PathfinderGame):
        """
        Draws board[c][r] with c = 0 and r = 0 being bottom left
        0 = empty (background color)
        1 = yellow
        -1 = red

        Args:
            game: The game to draw
        """
        origin = self.get_game_origin(game)

        # Draw on title of the game on the left of it
        img = self._font.render(game.teams[0].name, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + (self.n_cols * self.square_size) // 2,
            origin[1] - self._font.get_height() // 2,
        )
        self._screen.blit(img, rect)

        # Draw the squares - either as spaces if filled
        for r in range(len(game.board)):
            for c in range(len(game.board[0])):
                tile = game.board[r, c]
                color = (
                    YELLOW_COLOR
                    if tile == 1
                    else RED_COLOR
                    if tile == 2
                    else BLUE_COLOR
                    if (r, c) == game.position
                    else BACKGROUND_COLOR
                )

                pygame.gfxdraw.box(
                    self._screen,
                    (
                        origin[0] + c * self.square_size,
                        origin[1] + r * self.square_size,
                        self.square_size,
                        self.square_size,
                    ),
                    color,
                )

    def draw_win_message(self, game: PathfinderGame):
        """Displays win message on top of the board."""
        if game.completed:
            img = self._font.render(f"Score: {round(game.score, 1)}", True, BLACK_COLOR, None)
            rect = img.get_rect()
            origin = self.get_game_origin(game)
            rect.center = (
                origin[0] + (self.n_cols * self.square_size * 3) // 2,
                origin[1] + (self.n_rows * self.square_size) // 2,
            )

            self._screen.blit(img, rect)
