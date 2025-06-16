import random
from typing import List, Optional, Tuple

import pygame
import pygame.gfxdraw

from competition_controller import CompetitionController, wait_for_click
from stick_pile.game import StickPileGame
from head_to_head_viewer import HeadToHeadGameViewer


from events import Event


# colors
BLUE_COLOR = (23, 93, 222)
YELLOW_COLOR = (255, 240, 0)
RED_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (19, 72, 162)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
LIGHT_GRAY_COLOR = (200, 200, 200)

BACKGROUND_COLOR = LIGHT_GRAY_COLOR


class StickPileGameViewer(HeadToHeadGameViewer):
    GAME_HEIGHT = 10
    GAME_WIDTH = 8
    LANDSCAPE = True

    def __init__(self, controller: CompetitionController):
        self.team_a_color = BLACK_COLOR
        self.team_b_color = BLACK_COLOR
        self.BACKGROUND_COLOR = BACKGROUND_COLOR
        super().__init__(controller)
        self.stick_sprite = pygame.image.load(
            "src/stick_pile/stick.png"
        ).convert_alpha()

    def reset_games(self) -> None:
        super().reset_games()

    def draw_game(self, game: StickPileGame) -> None:

        origin = self.get_game_origin(game)

        if game.doing_reset:
            wait_for_click()

        # Draw title
        title = game.name.split(": ")[0]
        img = self._font.render(title, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] - self._font.get_height() // 3 - 10,
        )
        self._screen.blit(img, rect)

        title = f"Number of sticks remaining {game.number_of_sticks_remaining}"

        img = self._font.render(title, True, BLACK_COLOR, None)
        rect = img.get_rect()

        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] + self.pixel_game_height + self._font.get_height() * 3,
        )

        self._screen.blit(img, rect)
        # Teascore names and counters
        for idx, team in enumerate([game.team_a, game.team_b]):

            x_pos = origin[0] + idx * self.pixel_game_width
            y_pos = origin[1] + self.pixel_game_height - self._font.get_height()

            # Turn not switched if the game is over

            if game.most_recent_move is None:
                sticks_taken = " "
            elif game.round_over:
                if idx == 0 and game.env.player_move == "player":
                    sticks_taken = game.most_recent_move
                elif idx == 1 and game.env.player_move == "opponent":
                    sticks_taken = game.most_recent_move
                else:
                    sticks_taken = " "
            # Switched as the turn has already been switched
            elif idx == 0 and game.env.player_move == "opponent":
                sticks_taken = game.most_recent_move
            elif idx == 1 and game.env.player_move == "player":
                sticks_taken = game.most_recent_move
            else:
                sticks_taken = " "

            offset = self.pixel_game_width // 4
            if idx == 0:
                offset = offset * -1

            self.create_text(
                text=f"Took:\n{sticks_taken} stick(s)",
                color=YELLOW_COLOR if idx == 0 else RED_COLOR,
                pos=(
                    x_pos + offset,
                    y_pos + self._font.get_height(),
                ),
                font=self._font,
            )

            self.draw_score(origin, game)
            self.draw_team_names(origin, game)
        # # Draw background of the board
        # pygame.gfxdraw.box(
        #     self._screen,
        #     pygame.Rect(
        #         origin[0],
        #         origin[1],
        #         self.pixel_game_width,
        #         self.pixel_game_height,
        #     ),
        #     BLACK_COLOR,
        # )

        for n_stick in range(game.number_of_sticks_remaining):
            self.render_stick(origin, n_stick)

    def render_stick(self, origin: Tuple[int, int], n_stick: int) -> None:
        rotated_sprite = pygame.transform.rotate(
            self.stick_sprite,
            90,
        )
        sprite_rect = rotated_sprite.get_rect()
        target_width = int(self.pixel_game_width / 1.5)
        target_height = self.pixel_game_height

        sprite_aspect = sprite_rect.width / sprite_rect.height
        target_aspect = target_width / target_height

        if sprite_aspect > target_aspect:
            new_width = target_width
            new_height = int(target_width / sprite_aspect)
        else:
            new_height = target_height
            new_width = int(target_height * sprite_aspect)

        scaled_sprite = pygame.transform.scale(rotated_sprite, (new_width, new_height))

        game_rectangle = pygame.Rect(
            origin[0], origin[1], self.pixel_game_width, self.pixel_game_height
        )
        blit_position = scaled_sprite.get_rect()
        random.seed(n_stick)
        blit_position.centerx = (
            game_rectangle.centerx
            + self.pixel_game_width * 0.05 * random.uniform(-1, 1)
        )
        blit_position.bottom = game_rectangle.bottom - n_stick * (new_height // 1.2)

        self._screen.blit(scaled_sprite, blit_position)

    def draw_score(self, origin: Tuple[int, int], game: StickPileGame) -> None:
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

    def draw_win_message(self, game: StickPileGame) -> None:
        """Displays win message on top of the board."""
        if game.winner is not None and game.completed:
            img = self._font.render(
                f"{game.winner.name} won!",
                True,
                BLACK_COLOR if game.winner == game.team_a else WHITE_COLOR,
                YELLOW_COLOR if game.winner == game.team_a else RED_COLOR,
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

    def draw_team_names(self, origin: Tuple[int, int], game: StickPileGame) -> None:
        # Draw team names of the game on the left of it
        font = pygame.font.SysFont("arial", round(self.pixel_game_height / 10))

        self.create_text(
            text=game.team_a.name,
            color=YELLOW_COLOR,
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
            color=RED_COLOR,
            pos=(
                origin[0] + 5 * self.pixel_game_width // 4,
                origin[1] + self.pixel_game_height // 2,
            ),
            font=font,
            max_width=self.pixel_game_width // 4,
            background_color=None,
        )
