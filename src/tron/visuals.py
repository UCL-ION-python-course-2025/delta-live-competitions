import pygame

from head_to_head_viewer import HeadToHeadGameViewer
from observation import Observer
from tron.game import TronGame

BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
LIGHT_GRAY_COLOR = (200, 200, 200)


class TronGameViewer(HeadToHeadGameViewer):
    GAME_HEIGHT = 600
    GAME_WIDTH = 600
    LANDSCAPE = True

    def __init__(self, controller):
        super().__init__(controller)
        # Default is a bit big
        self._font = pygame.font.SysFont("arial", round(self.pixel_game_height / 12))

    def reset_games(self):
        super().reset_games()

    def draw_game(self, game: TronGame) -> None:
        origin = self.get_game_origin(game)

        subsurf = self._screen.subsurface(
            (origin[0], origin[1], self.pixel_game_height, self.pixel_game_width)
        )

        game.env.render_game(
            screen=subsurf,
        )

        # Draw the title
        title = game.name.split(": ")[0]
        img = self._font.render(title, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] - self._font.get_height() // 2,
        )
        self._screen.blit(img, rect)

        for idx, score in enumerate([game.team_a_score, game.team_b_score]):
            team = game.teams[idx]
            color = game.env.color_lookup[game.bike_names_map[team.name]]
            score_len = len(str(score))
            rect = pygame.Rect(
                origin[0]
                - self._font.get_height() * 5 * score_len // 4
                + idx * (self.pixel_game_width + self._font.get_height() * 3 * score_len // 2),
                origin[1],
                self._font.get_height() * score_len,
                self._font.get_height() * 3 // 2,
            )
            pygame.draw.rect(self._screen, LIGHT_GRAY_COLOR, rect, 0, 3)
            pygame.draw.rect(self._screen, BLACK_COLOR, rect, 1, 3)

            img = self._font.render(str(score), True, color, LIGHT_GRAY_COLOR)
            rect = img.get_rect()
            rect.center = (
                origin[0]
                - self._font.get_height() * 3 * score_len // 4
                + idx * (self.pixel_game_width + self._font.get_height() * 3 * score_len // 2),
                origin[1] + self._font.get_height() * 3 // 4,
            )
            self._screen.blit(img, rect)

            img = self._font.render(team.name, True, color, LIGHT_GRAY_COLOR)
            rect = img.get_rect()
            rect.center = (
                origin[0] + self.pixel_game_width * idx,
                origin[1] + self.pixel_game_height + self._font.get_height() // 2,
            )
            self._screen.blit(img, rect)

    def draw_win_message(self, game: TronGame):
        """Displays win message on top of the board."""
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
            origin[1] - self._font.get_height() // 2,
        )

        self._screen.blit(img, rect)
