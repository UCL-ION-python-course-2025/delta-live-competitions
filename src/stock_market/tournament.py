import math
import os
from typing import Tuple

import pygame

from game_parent import Game
from observation import Observable, Observer

from .game import StockGame

ASSET_PATH = "src/stock_market/assets"


class StockTournament(Observer):
    GAME_HEIGHT = 100
    GAME_WIDTH = 100
    MARGIN_TOP_LEADERBOARD = 120

    SPEED = 1

    def __init__(self, controller: "Observable"):
        super().__init__(controller)
        self.day_number = 0
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join(ASSET_PATH, "FreeSansBold.otf"), 35)

    def draw_game(self, game: StockGame) -> None:
        """Draws a game.

        Args:
            game: The game to draw
        """
        starting_pos = self.get_game_origin(game)

        game.set_starting_position(
            starting_pos[0] + self.pixel_game_width // 2,
            starting_pos[1] + self.pixel_game_height // 2,
        )
        scale = 1 / self.game_to_pixel_ratio
        game.draw_game(self._screen, scale=scale)
        game.display_team_name()
        self.day_number = game.n_rounds
        self.tournament_heading()

    def draw_win_message(self, game: Game) -> None:
        """Displays win message on top of the board."""
        pass

    def get_game_rows_cols(self) -> Tuple[int, int]:
        n_games = len(self.games)
        game_cols = 6 if n_games >= 10 else 5 if n_games >= 7 else 3 if n_games >= 3 else 2
        game_rows = math.ceil(len(self.games) / game_cols)
        return game_rows, game_cols

    def tournament_heading(self) -> None:
        self.create_text(
            "How much money can you make, starting with 1 Million dollars?!",
            (0, 0, 0),
            pos=(self._screen.get_width() // 2, 10 + self._font.get_linesize() // 2),
            font=self.font,
        )
        self.create_text(
            f"Day {self.day_number}",
            (0, 0, 0),
            pos=(
                self._screen.get_width() // 2,
                self._screen.get_height() - (3 * self._font.get_linesize()) // 2,
            ),
            font=self.font,
        )
