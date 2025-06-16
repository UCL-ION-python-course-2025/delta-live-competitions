import math

import numpy as np
import pygame
import pygame.gfxdraw

from competition_controller import CompetitionController
from observation import Observer
from twenty_forty_eight.game import TwentyFortyEightGame

# colors
BLUE_COLOR = (23, 93, 222)
YELLOW_COLOR = (255, 240, 0)
RED_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

BACKGROUND_COLOR = (186, 172, 159)
TILE_colorS = {
    0: (204, 192, 179),
    2: (238, 227, 217),
    4: (226, 223, 198),
    8: (242, 176, 121),
    16: (244, 148, 99),
    32: (245, 124, 96),
    64: (245, 94, 59),
    128: (236, 206, 115),
    256: (236, 203, 98),
    512: (236, 199, 80),
    1024: (236, 196, 63),
    2048: (236, 193, 45),
    4096: (101, 214, 149),
    8192: (97, 215, 145),
    16384: (35, 138, 86),
}


class TwentyFortyEightGameViewer(Observer):
    GAME_WIDTH = 1
    GAME_HEIGHT = 1

    def __init__(self, controller: CompetitionController):
        super().__init__(controller)
        self.n_rows = 4
        self.n_cols = 4

    def reset_games(self):
        super(TwentyFortyEightGameViewer, self).reset_games()
        # The 5/8 corresponds to the gaps between tiles
        self.tile_size = self.pixel_game_height // (4 + (5 / 8))
        self.gap_size = self.tile_size // 8
        self.draw_all_games()

    def draw_game(self, game: TwentyFortyEightGame):
        """Draws 2048 game state.

        TODO: Add sliding animations

        Args:
            game: The game to draw
        """
        origin = self.get_game_origin(game)

        # Draw on title of the game on the left of it
        img = self._font.render(game.teams[0].name, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + (self.n_cols * self.tile_size) // 2,
            origin[1] - self._font.get_height(),
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
            BACKGROUND_COLOR,
        )

        # Draw the squares - either as spaces if filled
        for row_idx, row in enumerate(game.board):
            for col_idx, tile in enumerate(row):
                tile_color = TILE_colorS.get(tile, (0, 0, 0))

                pygame.gfxdraw.box(
                    self._screen,
                    (
                        origin[0] + col_idx * (self.tile_size + self.gap_size) + self.gap_size,
                        origin[1] + row_idx * (self.tile_size + self.gap_size) + self.gap_size,
                        self.tile_size,
                        self.tile_size,
                    ),
                    tile_color,
                )
                if tile != 0:
                    str_length = len(str(tile))
                    self.create_text(
                        str(tile),
                        WHITE_COLOR if sum(tile_color) < 128 * 3 else BLACK_COLOR,
                        (
                            origin[0]
                            + col_idx * (self.tile_size + self.gap_size)
                            + self.gap_size
                            + self.tile_size // 2,
                            origin[1]
                            + row_idx * (self.tile_size + self.gap_size)
                            + self.gap_size
                            + self.tile_size // 2,
                        ),
                        pygame.font.SysFont(
                            "arial",
                            round((self.pixel_game_height // 5) / math.sqrt(str_length + 1)),
                            bold=True,
                        ),
                    )
        # Display last move made with an arrow
        if game.last_move is not None:
            arrow_length = self.pixel_game_height // 4

            def to_arrow_x(pos: int) -> int:
                return origin[0] - self.pixel_game_width // 2 + pos

            def to_arrow_y(pos: int) -> int:
                return origin[1] + self.pixel_game_height // 2 + pos

            arrow_points = {
                0: (
                    (0, 0),
                    (round(arrow_length * 2 / 3), 0),
                    (round(arrow_length / 3), -arrow_length),
                ),
                1: (
                    (round(arrow_length * 2 / 3), 0),
                    (round(arrow_length * 2 / 3), round(arrow_length * 2 / 3)),
                    (round(arrow_length * 5 / 3), round(arrow_length / 3)),
                ),
                2: (
                    (round(arrow_length * 2 / 3), round(arrow_length * 2 / 3)),
                    (0, round(arrow_length * 2 / 3)),
                    (round(arrow_length / 3), round(arrow_length * 5 / 3)),
                ),
                3: (
                    (0, round(arrow_length * 2 / 3)),
                    (0, 0),
                    (-arrow_length, round(arrow_length / 3)),
                ),
            }
            pygame.gfxdraw.filled_polygon(
                self._screen,
                [(to_arrow_x(x), to_arrow_y(y)) for (x, y) in arrow_points[game.last_move.value]],
                BLACK_COLOR,
            )

    def draw_win_message(self, game: TwentyFortyEightGame):
        """Displays win message on top of the board."""
        if game.completed:
            img = self._font.render(f"Score: {game.score}", True, BLACK_COLOR, None)
            rect = img.get_rect()
            origin = self.get_game_origin(game)
            rect.center = (
                origin[0] + self.pixel_game_width // 2,
                origin[1] + self.pixel_game_height + self._font.get_linesize(),
            )

            self._screen.blit(img, rect)

            img = self._font.render(f"Highest tile: {np.max(game.board)}", True, BLACK_COLOR, None)
            rect = img.get_rect()
            origin = self.get_game_origin(game)
            rect.center = (
                origin[0] + round(self.pixel_game_width * 1.5),
                origin[1] + self.pixel_game_height // 2 + self._font.get_linesize() * 2,
            )

            self._screen.blit(img, rect)
