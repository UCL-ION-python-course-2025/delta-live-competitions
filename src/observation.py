import math
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pygame
import pygame.gfxdraw

from events import Event
from game_parent import Game, HeadToHeadGame
from knockout_competition import KnockoutCompetition
from team import Team
from visual_utils import wrap_text

# Colors
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
LIGHT_GRAY_COLOR = (240, 240, 240)

# Podium colors
GOLD_COLOR = (255, 215, 0)
SILVER_COLOR = (192, 192, 192)
BRONZE_COLOR = (205, 127, 50)


class Observer(ABC):
    MARGIN_TOP_LEADERBOARD = 150
    GAME_MARGIN = 80  # pixels

    GAME_WIDTH = 0
    GAME_HEIGHT = 0
    EXTRA_WIDTH = 0
    EXTRA_HEIGHT = 0

    BACKGROUND_COLOR = LIGHT_GRAY_COLOR
    LANDSCAPE = False

    def __init__(self, controller: "Observable") -> None:

        self.controller = controller
        controller.add_observer(self)

        self.pixel_game_width = 0
        self.pixel_game_height = 0
        self.game_to_pixel_ratio = 0

        pygame.init()
        icon = pygame.image.load(f"{Path.cwd()}/delta_logo.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption(self.controller.name)
        self._screen = pygame.display.set_mode((800, 600))
        self.reset_games()
        self.clock = pygame.time.Clock()

    def reset_games(self) -> None:
        game_rows, game_cols = self.get_game_rows_cols()

        board_row_height = self._screen.get_height() / (game_rows + 1)
        board_col_width = self._screen.get_width() / (game_cols * 1.25)

        height_ratio = (board_row_height - self.GAME_MARGIN) / self.GAME_HEIGHT
        width_ratio = (board_col_width - self.GAME_MARGIN) / (
            self.GAME_WIDTH + 2 * self.EXTRA_WIDTH
        )

        self.game_to_pixel_ratio = min(height_ratio, width_ratio)

        self.pixel_game_width = round(
            (self.GAME_WIDTH + 2 * self.EXTRA_WIDTH) * self.game_to_pixel_ratio
        )
        self.pixel_game_height = round(self.GAME_HEIGHT * self.game_to_pixel_ratio)

        self.game_origins = self.get_origins(
            (self.pixel_game_width, self.pixel_game_height)
        )
        self._font = pygame.font.SysFont("arial", round(self.pixel_game_height / 10))

    def get_game_origin(self, game: Game) -> Tuple[int, int]:
        return self.game_origins[self.games.index(game)]

    def get_game_rows_cols(self) -> Tuple[int, int]:
        n_games = len(self.games)
        game_cols = (
            4 if n_games >= 10 else 3 if n_games >= 5 else 2 if n_games >= 3 else 1
        )
        game_rows = math.ceil(n_games / game_cols)
        return (game_cols, game_rows) if self.LANDSCAPE else (game_rows, game_cols)

    def get_origins(self, game_dims: Tuple[float, float]) -> Dict[int, Tuple[int, int]]:
        # Figure out the number of columns and rows of games
        game_rows, game_cols = self.get_game_rows_cols()

        board_row_height = self._screen.get_height() / (game_rows + 1)
        board_col_width = self._screen.get_width() / (game_cols * 2)

        origins = {}
        for count, game in enumerate(self.games):
            x_origin = board_col_width - game_dims[0] / 2
            # If 2 rows: if odd - right col. If even - left col
            x_origin += (count % game_cols) * 2 * board_col_width
            y_origin = board_row_height - game_dims[1] / 2
            # If odd, bottom row, if even, top row
            y_origin += (count // game_cols) * board_row_height
            origins[count] = (round(x_origin), round(y_origin))

        return origins

    @property
    def games(self) -> List[Game]:
        return [
            game
            for game in self.controller.current_round_of_games()
            # Include all non-HeadToHeadGames. Only check if robot-v-robot if HeadToHead
            #  since the is_robot_vs_robot_game property only exists for HeadToHeadGames
            if not (
                issubclass(type(game), HeadToHeadGame) and game.is_robot_vs_robot_game
            )
        ]

    def draw_all_games(self) -> None:
        """Draws all games in the current round."""
        self._screen.fill(self.BACKGROUND_COLOR)
        for game in self.games:
            self.draw_game(game)
            if game.completed:
                self.draw_win_message(game)
        pygame.display.update()
        self.clock.tick()

    @abstractmethod
    def draw_game(self, game: Game) -> None:
        """Draws a game.

        Args:
            game: The game to draw
        """
        pass

    def update(self, competition_controller, event: Event, *argv) -> None:
        """Called when notified.

        Updates the view.
        """
        if event == Event.GAME_RESET:
            self.reset_games()
        elif event == Event.STATE_CHANGE:
            self.draw_all_games()

    def create_text(
        self,
        text: str,
        color: Tuple[int, int, int],
        pos: Tuple[int, int],
        font: pygame.font.Font,
        max_width: Optional[int] = None,
        background_color: Optional[Tuple[int, int, int]] = None,
    ):

        lines = (
            wrap_text(text, font, max_width)
            if max_width is not None
            else text.replace("\t", "    ").split("\n")
        )

        line_ys = (
            np.arange(len(lines)) - len(lines) / 2 + 0.5
        ) * 1.25 * font.get_linesize() + pos[1]

        # Create the surface and rect that make up each line
        text_objects = []

        for line, y_pos in zip(lines, line_ys):
            text_surface = font.render(line, True, color, background_color)
            text_rect = text_surface.get_rect(center=(pos[0], y_pos))
            text_objects.append((text_surface, text_rect))

        # Render each line
        for text_object in text_objects:
            self._screen.blit(*text_object)

    @abstractmethod
    def draw_win_message(self, game: Game) -> None:
        """Displays win message on top of the board."""
        pass

    def draw_podium_and_leaderboard(self, ranking: Dict[int, List[Team]]) -> None:
        self._screen.fill(WHITE_COLOR)
        screen_width, screen_height = pygame.display.get_surface().get_size()
        text_height = 48
        podium_font = pygame.font.SysFont("arial", text_height)
        podium_width = 300
        margin_left = (screen_width - (3 * podium_width)) // 2
        # Gold
        pygame.gfxdraw.box(
            self._screen,
            pygame.Rect(
                margin_left + podium_width,
                self.MARGIN_TOP_LEADERBOARD + 1.5 * text_height,
                podium_width,
                text_height * 4,
            ),
            GOLD_COLOR,
        )
        self.create_text(
            "1",
            BLACK_COLOR,
            pos=(
                round(margin_left + 1.5 * podium_width),
                round(self.MARGIN_TOP_LEADERBOARD + 3.5 * text_height),
            ),
            font=podium_font,
        )
        self.create_text(
            " ".join([r.name for r in ranking[1]]),
            BLACK_COLOR,
            pos=(round(margin_left + 1.5 * podium_width), self.MARGIN_TOP_LEADERBOARD),
            font=podium_font,
            max_width=podium_width,
        )
        if 1 in ranking:
            ranking.pop(1)
        # Silver
        pygame.gfxdraw.box(
            self._screen,
            pygame.Rect(
                margin_left,
                self.MARGIN_TOP_LEADERBOARD + 2.5 * text_height,
                podium_width,
                text_height * 3,
            ),
            SILVER_COLOR,
        )
        self.create_text(
            "2",
            BLACK_COLOR,
            pos=(
                round(margin_left + podium_width // 2),
                round(self.MARGIN_TOP_LEADERBOARD + 4 * text_height),
            ),
            font=podium_font,
        )
        self.create_text(
            " ".join([r.name for r in ranking[2]]),
            BLACK_COLOR,
            pos=(
                round(margin_left + podium_width // 2),
                round(self.MARGIN_TOP_LEADERBOARD + text_height),
            ),
            font=podium_font,
            max_width=podium_width,
        )
        if 2 in ranking:
            ranking.pop(2)

        if 3 in ranking:
            # Bronze
            pygame.gfxdraw.box(
                self._screen,
                pygame.Rect(
                    margin_left + 2 * podium_width,
                    self.MARGIN_TOP_LEADERBOARD + 3.5 * text_height,
                    podium_width,
                    text_height * 2,
                ),
                BRONZE_COLOR,
            )
            self.create_text(
                "3",
                BLACK_COLOR,
                pos=(
                    round(margin_left + 2.5 * podium_width),
                    round(self.MARGIN_TOP_LEADERBOARD + 4.5 * text_height),
                ),
                font=podium_font,
            )
            self.create_text(
                " ".join([r.name for r in ranking[3]]),
                BLACK_COLOR,
                pos=(
                    round(margin_left + 2.5 * podium_width),
                    round(self.MARGIN_TOP_LEADERBOARD + 2 * text_height),
                ),
                font=podium_font,
                max_width=podium_width,
            )
            ranking.pop(3)
        if ranking:
            self.draw_leaderboard(
                ranking,
                podium_width * 3,
                round(self.MARGIN_TOP_LEADERBOARD + 5.5 * text_height),
            )

        pygame.display.update()

    def draw_leaderboard(
        self, ranking: Dict[int, List[Team]], leaderboard_width: int, margin_top: int
    ) -> None:
        margin_top += 24
        num_teams = sum(len(teams) for teams in ranking.values())
        font = pygame.font.SysFont(
            "arial", 48 if num_teams < 4 else round(96 / math.sqrt(num_teams))
        )
        row_height = (
            pygame.display.get_surface().get_height() - margin_top
        ) // num_teams
        highest_rank = min(ranking.keys())
        for rank, teams in sorted(ranking.items()):
            # Normalised rank (ranking in ranking dict)
            normalised_rank = rank - highest_rank
            for count, team in enumerate(teams):
                pygame.gfxdraw.box(
                    self._screen,
                    pygame.Rect(
                        (pygame.display.get_surface().get_width() - leaderboard_width)
                        // 2,
                        margin_top + (row_height * (normalised_rank + count)),
                        leaderboard_width,
                        row_height,
                    ),
                    (220, 220, 220),
                )
                pygame.gfxdraw.rectangle(
                    self._screen,
                    pygame.Rect(
                        (pygame.display.get_surface().get_width() - leaderboard_width)
                        // 2,
                        margin_top + (row_height * (normalised_rank + count)),
                        leaderboard_width,
                        row_height,
                    ),
                    BLACK_COLOR,
                )
                self.create_text(
                    f"{rank}",
                    BLACK_COLOR,
                    pos=(
                        (
                            (
                                pygame.display.get_surface().get_width()
                                - leaderboard_width
                                + 2 * font.get_height()
                            )
                            // 2
                        ),
                        margin_top + (row_height * ((normalised_rank + count) + 0.5)),
                    ),
                    font=font,
                )
                self.create_text(
                    team.name,
                    BLACK_COLOR,
                    pos=(
                        ((pygame.display.get_surface().get_width()) // 2),
                        margin_top + (row_height * ((normalised_rank + count) + 0.5)),
                    ),
                    font=font,
                )

    def draw_knockout_tournament_tree(self, competition: KnockoutCompetition) -> None:
        competition.tournament_tree_visualised = True
        self._screen.fill(WHITE_COLOR)
        screen_width, screen_height = pygame.display.get_surface().get_size()

        # Write title at the top
        title_font = pygame.font.SysFont("arial", 64)
        self.create_text(
            competition.name,
            BLACK_COLOR,
            pos=(screen_width // 2, title_font.get_linesize()),
            font=title_font,
        )

        margin_x = 60

        team_names = competition.get_team_names()

        # Draw tree skeletons
        first_tree_origin = (
            margin_x,
            round(self.MARGIN_TOP_LEADERBOARD + title_font.get_linesize() * 1.5),
        )
        tree_width = screen_width - 2 * margin_x - 20
        tree_height = round(
            screen_height
            - 2 * self.MARGIN_TOP_LEADERBOARD
            - title_font.get_linesize() * 1.5
        )
        if len(team_names[0]) <= 8:
            self.draw_tournament_tree_skeleton(
                origin=first_tree_origin,
                dims=(tree_width, tree_height),
                team_names=team_names,
                reverse=False,
                round_names=competition.get_round_names(),
            )
        else:
            self.draw_tournament_tree_skeleton(
                origin=first_tree_origin,
                dims=(tree_width // 2, tree_height),
                team_names=[
                    teams[: len(teams) // 2] for teams in team_names if len(teams) >= 2
                ],
                reverse=False,
                round_names=competition.get_round_names(),
            )
            self.draw_tournament_tree_skeleton(
                origin=(20 + screen_width // 2, first_tree_origin[1]),
                dims=(tree_width // 2, tree_height),
                team_names=[
                    teams[len(teams) // 2 :] for teams in team_names if len(teams) >= 2
                ],
                reverse=True,
                round_names=competition.get_round_names(),
            )

        pygame.display.update()

    def draw_tournament_tree_skeleton(
        self,
        origin: Tuple[int, int],
        dims: Tuple[int, int],
        team_names: List[List[str]],
        reverse: bool,
        round_names: List[str],
    ):
        """
        Args:
            origin:
            dims: Dimensions of the rectangle (x, y) in pixel-coordinates that the tournament tree
                skeleton should fill
            team_names: List of lists of teams in each round, the order here is top to bottom
            reverse: Whether to reverse the direction the tree
        """

        def to_screen_x(x: float) -> int:
            """Transform a relative x position into absolute screen pixel position."""
            return round(origin[0] + x if not reverse else origin[0] + dims[0] - x)

        num_rounds = math.ceil(math.log2(len(team_names[0])))
        font = pygame.font.SysFont("arial", 64 // num_rounds)
        bold_font = pygame.font.SysFont("arial", 64 // num_rounds, bold=True)

        line_width = dims[0] // len(team_names)
        for round_num, round_team_names in enumerate(team_names):
            top_offset = (2**round_num) * (dims[1] // len(team_names[0])) // 2
            line_height = (2**round_num) * dims[1] // len(team_names[0])

            if round_num < len(round_names):
                self.create_text(
                    round_names[round_num].split(" of ")[0],
                    BLACK_COLOR,
                    pos=(
                        to_screen_x(line_width * (round_num + 0.5)),
                        origin[1] - font.get_linesize() * 2,
                    ),
                    font=bold_font,
                )

            for team_count, team_name in enumerate(round_team_names):
                pygame.gfxdraw.hline(
                    self._screen,
                    to_screen_x(line_width * round_num),
                    to_screen_x(line_width * (round_num + 1)),
                    top_offset + origin[1] + team_count * line_height,
                    BLACK_COLOR,
                )
                self.create_text(
                    team_name,
                    BLACK_COLOR,
                    pos=(
                        to_screen_x(line_width * (round_num + 0.5)),
                        top_offset
                        + origin[1]
                        + team_count * line_height
                        - font.get_linesize() // 2,
                    ),
                    font=(
                        font
                        if len(round_team_names) == 1
                        or len(round_team_names) > 1
                        and team_name not in team_names[round_num + 1]
                        else bold_font
                    ),
                )
            if len(round_team_names) > 1:
                for team_name_idx in range(0, len(round_team_names), 2):
                    pygame.gfxdraw.vline(
                        self._screen,
                        to_screen_x(line_width * (round_num + 1)),
                        top_offset + origin[1] + (team_name_idx + 1) * line_height,
                        top_offset + origin[1] + team_name_idx * line_height,
                        BLACK_COLOR,
                    )

    def tournament_heading(self) -> None:
        pass

    def get_rules(self) -> None:
        pass

    def show_rules(self):

        font = pygame.font.SysFont("arial", 32)
        bold_font = pygame.font.SysFont("arial", 32, bold=True)

        rules = self.get_rules()
        if rules is None:
            return
        self._screen.fill(WHITE_COLOR)

        self.create_text(
            f"{self.controller.name} Rules",
            BLACK_COLOR,
            pos=(self._screen.get_width() // 2, self._screen.get_height() // 10),
            font=bold_font,
        )

        self.create_text(
            rules,
            BLACK_COLOR,
            pos=(self._screen.get_width() // 2, self._screen.get_height() // 2),
            font=font,
        )
        pygame.display.update()


class Observable:
    def __init__(self, name: str):
        self.name = name
        self._observers: List[Observer] = []

    def notify(self, event: Event, *argv) -> None:
        for obs in self._observers:
            obs.update(self, event, *argv)

    def redraw(self) -> None:
        self.notify(Event.STATE_CHANGE)

    def add_observer(self, obs: Observer) -> None:
        self._observers.append(obs)

    def remove_observer(self, obs: Observer) -> None:
        if obs in self._observers:
            self._observers.remove(obs)

    def current_round_of_games(self) -> List[Game]:
        """Added for type-checking!"""
        raise NotImplementedError
