import math
import time
from typing import Tuple

import numpy as np
import pygame

from competition_controller import CompetitionController
from events import Event
from game_parent import Game
from observation import Observable, Observer

from .game import WordleGame


class WorldleTournament(Observer):
    GAME_HEIGHT = 100
    GAME_WIDTH = 100
    MARGIN_TOP_LEADERBOARD = 10

    N_ROUNDS_TOTAL = 10

    def __init__(self, controller: "Observable"):
        super().__init__(controller)
        self.n_rounds = 0

    def draw_game(self, game: WordleGame) -> None:
        """Draws a game.

        Args:
            game: The game to draw
        """
        starting_pos = self.get_game_origin(game)
        game.visualisation_controller.set_starting_position(
            starting_pos[0], starting_pos[1]
        )

        scale = 1 / self.game_to_pixel_ratio
        game.visualisation_controller.draw_game(self._screen, scale=scale)
        game.visualisation_controller.draw_outline()
        game.visualisation_controller.display_team_name()

        self.tournament_heading()

    def draw_win_message(self, game: Game) -> None:
        """Displays win message on top of the board."""
        pass

    def get_game_rows_cols(self) -> Tuple[int, int]:
        n_games = len(self.games)
        game_cols = (
            6 if n_games >= 10 else 5 if n_games >= 5 else 4 if n_games >= 3 else 2
        )
        game_rows = math.ceil(len(self.games) / game_cols)
        return game_rows, game_cols

    def update(
        self, competition_controller: CompetitionController, event: Event, *argv: Tuple
    ) -> None:
        if self.n_rounds == self.N_ROUNDS_TOTAL - 1:  # lol
            return  # Game finished
        if event == Event.STATE_CHANGE:
            random_seed = np.random.randint(0, high=100000)
            self.n_rounds += 1
            while True:  # Starts a new round with a new word
                if pygame.event.get(pygame.MOUSEBUTTONUP):
                    self._screen.fill(pygame.Color("white"))
                    # self.write_all_team_names()
                    games = self.controller.current_round_of_games()
                    for game in games:
                        game.reset_game()
                        game.reset(random_seed=random_seed)
                    self.reset_visualisation()
                    self.tournament_heading()
                    time.sleep(2)
                    return

    def reset_visualisation(self) -> None:
        """Writes all team names."""
        games = self.controller.current_round_of_games()
        for game in games:
            game.visualisation_controller.display_team_name()
            game.visualisation_controller.draw_outline()
            game.visualisation_controller.display_score(
                game.n_rounds_solved, game.n_total_guesses
            )

    def tournament_heading(self) -> None:

        games = self.controller.current_round_of_games()
        assert (
            len(set([game._word for game in games])) == 1
        ), "All games must have the same word"
        current_word = games[0]._word
        pos = (
            self._screen.get_width() // 2,
            self.MARGIN_TOP + self._font.get_linesize() // 2,
        )
        heading_font = pygame.font.SysFont(
            "arial", round(self.pixel_game_height * 2 / 8)
        )
        self.create_text(f"Answer: {current_word}", (0, 0, 0), pos, font=heading_font)
        pygame.display.update()
        time.sleep(0.5)
