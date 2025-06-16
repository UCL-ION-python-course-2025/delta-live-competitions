import pygame
import pygame.gfxdraw

from delta_pong.game_mechanics import COURT_HEIGHT, COURT_WIDTH
from head_to_head_viewer import HeadToHeadGameViewer
from pong.game import PongGame

# colors
BLUE_COLOR = (23, 93, 222)
YELLOW_COLOR = (255, 240, 0)
RED_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (19, 72, 162)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
LIGHT_GRAY_COLOR = (200, 200, 200)


class PongGameViewer(HeadToHeadGameViewer):
    GAME_MARGIN = 120

    EXTRA_WIDTH = 20
    GAME_HEIGHT = COURT_HEIGHT
    GAME_WIDTH = COURT_WIDTH
    CINEMATIC_MODE = True

    def draw_game(self, game: PongGame):
        """Draws match game on screen.

        Args:
            game: The game to draw
        """
        origin = self.get_game_origin(game)

        # Draw team names of the game on the left of it
        font = pygame.font.SysFont("arial", round(self.pixel_game_height / 10))
        if not self.CINEMATIC_MODE:
            for count, (text, bg_color) in enumerate(
                zip(
                    [game.team_a.name, "vs", game.team_b.name],
                    [YELLOW_COLOR, None, RED_COLOR],
                )
            ):
                self.create_text(
                    text=text,
                    color=BLACK_COLOR,
                    pos=(
                        origin[0] - self.pixel_game_width // 2,
                        origin[1]
                        + self.pixel_game_height // 2
                        + int((count - 1) * font.get_linesize() * 1.25),
                    ),
                    font=font,
                    max_width=280,
                    background_color=bg_color,
                )
        else:
            self.create_text(
                text=game.team_a.name,
                color=BLACK_COLOR,
                pos=(
                    origin[0] - self.pixel_game_width // 4,
                    origin[1] + self.pixel_game_height // 2,
                ),
                font=font,
                max_width=self.pixel_game_width // 4,
                background_color=None,
            )
            self.create_text(
                text=game.team_b.name,
                color=BLACK_COLOR,
                pos=(
                    origin[0] + 5 * self.pixel_game_width // 4,
                    origin[1] + self.pixel_game_height // 2,
                ),
                font=font,
                max_width=self.pixel_game_width // 4,
                background_color=None,
            )

        # Draw the title
        title = game.name.split(": ")[0]
        img = self._font.render(title, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] - self._font.get_height() // 2 - 10,
        )

        # This used to be part of CINEMATIC_MODE, but titles
        # are written over each other
        # font = pygame.font.SysFont("arial", 64)
        # img = font.render(title, True, BLACK_COLOR, None)
        # rect = img.get_rect()
        # rect.center = (
        #     self._screen.get_width() // 2,
        #     font.get_linesize(),
        # )
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
            LIGHT_GRAY_COLOR,
        )

        # Draw the paddles
        pygame.gfxdraw.box(
            self._screen,
            pygame.Rect(
                # Maybe change signs below!
                origin[0],
                origin[1] + (game.env.paddle_1.bottom * self.game_to_pixel_ratio),
                (self.EXTRA_WIDTH * self.game_to_pixel_ratio),
                round(game.env.paddle_1.height * self.game_to_pixel_ratio),
            ),
            YELLOW_COLOR,
        )
        pygame.gfxdraw.box(
            self._screen,
            pygame.Rect(
                origin[0]
                + round((self.EXTRA_WIDTH + COURT_WIDTH) * self.game_to_pixel_ratio),
                origin[1] + round(game.env.paddle_2.bottom * self.game_to_pixel_ratio),
                (self.EXTRA_WIDTH * self.game_to_pixel_ratio),
                round(game.env.paddle_2.height * self.game_to_pixel_ratio),
            ),
            RED_COLOR,
        )

        # Draw the ball
        # Anti-aliased circle drawing
        pygame.gfxdraw.aacircle(
            self._screen,
            origin[0]
            + round((self.EXTRA_WIDTH + game.env.ball.x) * self.game_to_pixel_ratio),
            origin[1] + round(game.env.ball.y * self.game_to_pixel_ratio),
            int(
                1.5 * game.env.ball.radius * self.game_to_pixel_ratio
            ),  # 1.5 is to make it look bigger
            BLACK_COLOR,
        )

        pygame.gfxdraw.filled_circle(
            self._screen,
            origin[0]
            + round((self.EXTRA_WIDTH + game.env.ball.x) * self.game_to_pixel_ratio),
            origin[1] + round(game.env.ball.y * self.game_to_pixel_ratio),
            int(1.5 * game.env.ball.radius * self.game_to_pixel_ratio),
            BLACK_COLOR,
        )

        # Draw the walls
        pygame.gfxdraw.rectangle(
            self._screen,
            pygame.Rect(
                origin[0],
                origin[1],
                self.pixel_game_width,
                self.pixel_game_height,
            ),
            BLACK_COLOR,
        )

        # Draw the score
        for count, (score, color) in enumerate(
            [(game.team_a_score, YELLOW_COLOR), (game.team_b_score, RED_COLOR)]
        ):
            score_len = len(str(score))
            rect = pygame.Rect(
                origin[0]
                - self._font.get_height() * 5 * score_len // 4
                + count
                * (
                    self.pixel_game_width + self._font.get_height() * 3 * score_len // 2
                ),
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
                + count
                * (
                    self.pixel_game_width + self._font.get_height() * 3 * score_len // 2
                ),
                origin[1] + self._font.get_height() * 3 // 4,
            )
            self._screen.blit(img, rect)

        font = pygame.font.SysFont("arial", round(self.pixel_game_height / 10))
        img = font.render(
            f"Ball speed: {round(game.env.ball.speed, 2)}", True, BLACK_COLOR, None
        )
        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] + self.pixel_game_height + self._font.get_height(),
        )
        self._screen.blit(img, rect)

    def draw_win_message(self, game: PongGame):
        """Displays win message on top of the board."""
        if game.winner is not None and game.completed:
            img = self._font.render(
                f"{game.winner.name} won!",
                True,
                BLACK_COLOR if game.winner == game.team_a else WHITE_COLOR,
                YELLOW_COLOR if game.winner == game.team_a else RED_COLOR,
            )
        else:
            # pass
            img = self._font.render("Draw", True, WHITE_COLOR, BLUE_COLOR)

        rect = img.get_rect()
        origin = self.get_game_origin(game)
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] + self.pixel_game_height // 2,
        )

        self._screen.blit(img, rect)
