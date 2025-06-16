from typing import List, Optional, Tuple

from competition_controller import CompetitionController
from head_to_head_viewer import HeadToHeadGameViewer

from .game import PokerGame

DISC_SIZE_RATIO = 0.8

BLUE_COLOR = (23, 93, 222)
BACKGROUND_COLOR = (0, 101, 25)
YELLOW_COLOR = (255, 240, 0)


BLACK_COLOR = (6, 9, 16)
GRAY_COLOR = (102, 102, 122)
WHITE_COLOR = (255, 255, 255)

TEAM_NAME_COLOR = BLACK_COLOR

RED_COLOR = (255, 0, 0)
LIGHT_GRAY_COLOR = (200, 200, 200)


class PokerGameViewer(HeadToHeadGameViewer):
    GAME_HEIGHT = 10
    GAME_WIDTH = 8
    LANDSCAPE = True

    def __init__(self, controller: CompetitionController):
        super().__init__(controller)
        self.team_a_color = WHITE_COLOR
        self.team_b_color = BLACK_COLOR
        self.win_sequence: List[Optional[Tuple[int, int, int]]] = [None] * 3
        self.BACKGROUND_COLOR = BACKGROUND_COLOR

    def reset_games(self) -> None:
        super().reset_games()

    def draw_game(self, game: PokerGame) -> None:

        origin = self.get_game_origin(game)
        subsurf = self._screen.subsurface(
            (
                origin[0],
                origin[1],
                self.pixel_game_width,
                self.pixel_game_height,
            )
        )

        winner = game.team_a.name if game.env.reward > 0 else game.team_b.name
        game.env.render_game_tournament(
            screen=subsurf,
            font=self._font,
            win_message=(
                f"{winner} wins {abs(game.env.reward)} chips"
                if game.env.hand_done
                else None
            ),
        )

        img = self._font.render(
            f"{game.team_a.name}", True, BLACK_COLOR, LIGHT_GRAY_COLOR
        )

        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] + self.pixel_game_height + self._font.get_height(),
        )
        self._screen.blit(img, rect)

        img = self._font.render(
            f"{game.team_b.name}", True, BLACK_COLOR, LIGHT_GRAY_COLOR
        )
        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] - self._font.get_height(),
        )
        self._screen.blit(img, rect)

    def draw_win_message(self, game: PokerGame):
        """Displays win message on center of the board."""

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
            origin[1] + self.pixel_game_height // 2 + self._font.get_height() // 2,
        )

        self._screen.blit(img, rect)

    def get_game_rows_cols(self) -> Tuple[int, int]:
        return 1, len(self.games)
