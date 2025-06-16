from typing import List, Optional, Tuple

import pygame

from competition_controller import CompetitionController
from delta_go.game_mechanics import BLACK, KOMI, MAX_NUM_MOVES, WHITE, render_game
from delta_go.game_mechanics import score as game_scorer
from go.game import GoGame
from head_to_head_viewer import HeadToHeadGameViewer

DISC_SIZE_RATIO = 0.8

BLUE_COLOR = (23, 93, 222)
YELLOW_COLOR = (255, 240, 0)


BLACK_COLOR = (6, 9, 16)
GRAY_COLOR = (102, 102, 122)
WHITE_COLOR = BACKGROUND_COLOR = (255, 255, 255)

TEAM_NAME_COLOR = BLACK_COLOR

BLUE_COLOR = (23, 93, 222)
YELLOW_COLOR = (255, 240, 0)
RED_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
LIGHT_GRAY_COLOR = (200, 200, 200)

# Map colors in the Game object to rgb values
COLOR_MAP = {BLACK: BLACK_COLOR, WHITE: WHITE_COLOR}


class GoGameViewer(HeadToHeadGameViewer):
    GAME_HEIGHT = 10
    GAME_WIDTH = 8
    LANDSCAPE = True

    def __init__(self, controller: CompetitionController):
        self.team_a_color = WHITE_COLOR
        self.team_b_color = BLACK_COLOR
        self.win_sequence: List[Optional[Tuple[int, int, int]]] = [None] * 3
        self.BACKGROUND_COLOR = BACKGROUND_COLOR
        super().__init__(controller)

    def reset_games(self) -> None:
        super().reset_games()

    def draw_game(self, game: GoGame) -> None:

        origin = self.get_game_origin(game)

        # Draw title
        title = game.name.split(": ")[0]
        img = self._font.render(title, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] - self._font.get_height() // 3 - 10,
        )
        self._screen.blit(img, rect)

        # Draw number of turns taken
        title = f"Moves taken: {len(game.env.state.recent_moves)}/{MAX_NUM_MOVES}"
        img = self._font.render(title, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] + self.pixel_game_height + self._font.get_height() * 3,
        )
        self._screen.blit(img, rect)

        subsurf = self._screen.subsurface(
            (
                origin[0],
                origin[1],
                self.pixel_game_width,
                self.pixel_game_height,
            )
        )

        render_game(board=game.env.state.board, screen=subsurf, update_display=False)

        team_a_counter_color = COLOR_MAP[game.env.player_color]
        team_b_counter_color = (
            WHITE_COLOR if team_a_counter_color == BLACK_COLOR else BLACK_COLOR
        )

        team_a_is_black = team_a_counter_color == BLACK_COLOR

        # Team names and counters
        black_score, white_score = game_scorer(
            game.env.state.board, KOMI, return_both_colors=True
        )

        for idx, team in enumerate([game.team_a, game.team_b]):

            x_pos = origin[0] + idx * self.pixel_game_width
            y_pos = origin[1] + self.pixel_game_height - self._font.get_height()

            if idx == 0 and team_a_is_black or idx == 1 and not team_a_is_black:
                score = black_score
            else:
                score = white_score

            self.create_text(
                text=team.name,
                color=TEAM_NAME_COLOR,
                pos=(x_pos, y_pos),
                font=self._font,
            )

            self.create_text(
                text=f"Score: {score}",
                color=TEAM_NAME_COLOR,
                pos=(x_pos, y_pos + self._font.get_height()),
                font=self._font,
            )

            # Add the counter to the team name
            draw_counter(
                self._screen,
                x_pos=x_pos,
                y_pos=y_pos + self._font.get_height() * 2,
                size=self._font.get_height() // 2,
                outline_color=BLACK_COLOR,
                fill_color=[team_a_counter_color, team_b_counter_color][idx],
            )

    def draw_win_message(self, game: GoGame):
        """Displays win message on top of the board."""
        assert game.winner is not None
        img = self._font.render(
            f"{game.winner.name} won!",
            True,
            BLACK_COLOR if sum(game.winner_color) > 255 * 3 / 2 else WHITE_COLOR,
            game.winner_color,
        )

        rect = img.get_rect()
        origin = self.get_game_origin(game)
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] + self.pixel_game_height + self._font.get_height(),
        )

        self._screen.blit(img, rect)


def draw_counter(
    screen: pygame.surface.Surface,
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
