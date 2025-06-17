import math
from typing import Optional

import pygame
import pygame.gfxdraw
from pygame import Surface, Vector2
from pygame.transform import rotozoom

from competition_controller import CompetitionController
from delta_shooter.game_mechanics import NEON_GREEN, GameObject, ShooterEnv, load_sprite
from head_to_head_viewer import HeadToHeadGameViewer
from shooter.game import PLAYER_ONE_COLOR, PLAYER_TWO_COLOR, ShooterGame

BLUE_COLOR = (23, 93, 222)
YELLOW_COLOR = (255, 240, 0)
RED_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (19, 72, 162)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
LIGHT_GRAY_COLOR = (200, 200, 200)

UP = pygame.Vector2(0, -1)

# Size is set dymanically so pull it out of the class
GAME_SIZE = ShooterEnv(lambda x: x, half_sized_game=False).game_size


class ShooterGameViewer(HeadToHeadGameViewer):
    GAME_HEIGHT = GAME_SIZE[1]
    GAME_WIDTH = GAME_SIZE[0]
    LANDSCAPE = True

    def __init__(self, controller: CompetitionController):
        super().__init__(controller)
        self.space_original = load_sprite("space", False)
        self.background = pygame.transform.scale(
            self.space_original,
            (
                self.GAME_WIDTH * self.game_to_pixel_ratio,
                self.GAME_HEIGHT * self.game_to_pixel_ratio,
            ),
        )
        self.sprites = {
            "spaceship_player1": load_sprite("spaceship_player1"),
            "spaceship_player2": load_sprite("spaceship_player2"),
            "bullet": load_sprite("bullet"),
        }

        for k, v in self.sprites.items():
            if k != "bullet":
                self.sprites[k] = pygame.transform.scale(
                    v, (40 * self.game_to_pixel_ratio, 40 * self.game_to_pixel_ratio)
                )

    def game_obj_to_sprite(self, game_obj: GameObject) -> Optional[Surface]:
        if game_obj.name == "spaceship":
            return self.sprites[f"spaceship_player{game_obj.player}"]
        elif game_obj.name == "bullet":
            return self.sprites["bullet"]
        else:
            return None

    def draw_game(self, game: ShooterGame) -> None:
        """Draws match game on screen.

        Args:
            game: The game to draw
        """
        # Default font is a bit too big
        self._font = pygame.font.SysFont("arial", round(self.pixel_game_height / 11))
        self.background = pygame.transform.scale(
            self.space_original,
            (
                self.GAME_WIDTH * self.game_to_pixel_ratio,
                self.GAME_HEIGHT * self.game_to_pixel_ratio,
            ),
        )
        self.sprites = {
            "spaceship_player1": load_sprite("spaceship_player1"),
            "spaceship_player2": load_sprite("spaceship_player2"),
            "bullet": load_sprite("bullet"),
        }

        for k, v in self.sprites.items():
            if k != "bullet":
                self.sprites[k] = pygame.transform.scale(
                    v, (40 * self.game_to_pixel_ratio, 40 * self.game_to_pixel_ratio)
                )
        origin = self.get_game_origin(game)

        self._screen.blit(self.background, origin)

        for game_object in game.env._get_game_objects():
            sprite = self.game_obj_to_sprite(game_object)

            if game_object.name == "spaceship":

                if not game_object.dead:
                    angle = game_object.direction.angle_to(UP)
                    rotated_surface = rotozoom(sprite, angle, 1.0)
                    rotated_surface_size = Vector2(rotated_surface.get_size())
                    blit_position = (
                        pygame.Vector2(origin)
                        + game_object.position * self.game_to_pixel_ratio
                        - rotated_surface_size * 0.5
                    )
                    self._screen.blit(rotated_surface, blit_position)

            elif game_object.name == "bullet":
                blit_position = (
                    pygame.Vector2(origin)
                    + game_object.position * self.game_to_pixel_ratio
                )
                self._screen.blit(sprite, blit_position)

            elif game_object.name == "barrier":
                start = (
                    pygame.Vector2(origin)
                    + pygame.Vector2(game_object.corner1) * self.game_to_pixel_ratio
                )
                end = (
                    pygame.Vector2(origin)
                    + pygame.Vector2(game_object.corner2) * self.game_to_pixel_ratio
                )
                pygame.draw.line(
                    self._screen,
                    NEON_GREEN,
                    start,
                    end,
                    int(game_object.width * self.game_to_pixel_ratio),
                )

        # Draw team names of the game on the left of it
        team_a_width = self._font.render(
            game.team_a.name, True, WHITE_COLOR
        ).get_width()
        names_y_pos = origin[1] + self.pixel_game_height + self._font.get_height() // 2
        self.create_text(
            text=game.team_a.name,
            color=BLACK_COLOR,
            pos=(origin[0], names_y_pos),
            font=self._font,
            max_width=team_a_width,
            background_color=game.team_a_color,
        )
        team_b_width = self._font.render(
            game.team_b.name, True, WHITE_COLOR
        ).get_width()
        self.create_text(
            text=game.team_b.name,
            color=BLACK_COLOR,
            pos=(
                origin[0] + self.pixel_game_width,
                names_y_pos,
            ),
            font=self._font,
            max_width=team_b_width,
            background_color=game.team_b_color,
        )

        # Draw the timer
        time_remaining = str(math.ceil(game.MAX_TIME - game.time_elapsed))
        self.create_text(
            text=time_remaining,
            color=WHITE_COLOR,
            pos=(
                origin[0] + self.pixel_game_width // 2,
                origin[1] + self.pixel_game_height + self._font.get_height() // 2 + 2,
            ),
            font=self._font,
            max_width=team_b_width,
            background_color=BLACK_COLOR,
        )

        # Draw the title
        title = game.name.split(": ")[0]
        img = self._font.render(title, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] - self._font.get_height() // 2 - 10,
        )

        self._screen.blit(img, rect)

        # Draw the score
        font = self._font
        img = font.render(
            str(game.team_a_score), True, PLAYER_ONE_COLOR, LIGHT_GRAY_COLOR
        )
        rect = img.get_rect()
        rect.center = (
            origin[0] - font.get_height() // 2,
            origin[1] + font.get_height() // 2,
        )
        self._screen.blit(img, rect)

        img = font.render(
            str(game.team_b_score), True, PLAYER_TWO_COLOR, LIGHT_GRAY_COLOR
        )
        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width + font.get_height() // 2,
            origin[1] + font.get_height() // 2,
        )

        self._screen.blit(img, rect)

    def draw_win_message(self, game: ShooterGame) -> None:
        """Displays win message on top of the board."""
        if game.winner is not None and game.completed:
            img = self._font.render(
                f"{game.winner.name} won!",
                True,
                BLACK_COLOR if game.winner == game.team_a else WHITE_COLOR,
                PLAYER_ONE_COLOR if game.winner == game.team_a else PLAYER_TWO_COLOR,
            )
        else:
            img = self._font.render("Draw", True, WHITE_COLOR, BLUE_COLOR)

        rect = img.get_rect()
        origin = self.get_game_origin(game)
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] + self.pixel_game_height // 2,
        )

        self._screen.blit(img, rect)

    def get_rules(self):
        return (
            f"Space battles are played one on one.\n\n"
            f"The game is comprised of up to {2*ShooterGame.WIN_THRESHOLD - 1} rounds.\n\n"
            f"You win a round by shooting your opponent's ship\n\n"
            f"A round is drawn if both ships are destroyed at the same time or if a {ShooterGame.MAX_TIME} second timer expires\n\n"
            f"The first player to {ShooterGame.WIN_THRESHOLD} points wins\n\n"
            f"If two players cannot be separated after {2*ShooterGame.WIN_THRESHOLD-1} rounds, a tie is declared.\n"
        )
