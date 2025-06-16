from typing import Optional

import pygame
import pygame.gfxdraw

from game_parent import HeadToHeadGame
from observation import Observer

# Colors
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)


class HeadToHeadGameViewer(Observer):
    def reset_games(self):
        super(HeadToHeadGameViewer, self).reset_games()

    def draw_win_message(
        self,
        game: HeadToHeadGame,
        position: str = "bottom",
        font_size_override: Optional[int] = None,
    ):

        if font_size_override is not None:
            font = pygame.font.SysFont("arial", font_size_override)
        else:
            font = self._font

        """Displays win message on top of the board."""
        assert position in {"top", "middle", "bottom"}

        if (
            game.winner is not None
            and game.completed
            and not game.both_teams_progressing
        ):
            img = font.render(
                f"{game.winner.name} won!",
                True,
                BLACK_COLOR if sum(game.winner_color) > 255 * 3 / 2 else WHITE_COLOR,
                game.winner_color,
            )
        else:
            img = font.render("Draw", True, WHITE_COLOR, BLACK_COLOR)

        origin = self.get_game_origin(game)
        if position == "bottom":
            y_pos = origin[1] + self.pixel_game_height + font.get_height() // 2
        elif position == "middle":
            y_pos = origin[1] + self.pixel_game_height // 2
        elif position == "top":
            y_pos = origin[1] - font.get_height() // 2

        rect = img.get_rect()
        rect.center = (origin[0] + self.pixel_game_width // 2, y_pos)

        self._screen.blit(img, rect)
