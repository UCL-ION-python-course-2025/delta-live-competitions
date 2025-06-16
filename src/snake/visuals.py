import math
from typing import Dict, Tuple

import pygame
import pygame.gfxdraw

from competition_controller import CompetitionController
from observation import Observer
from snake.competitor_code import ARENA_HEIGHT, ARENA_WIDTH, BLOCK_SIZE, Snake
from snake.game import SnakeGame

# colors
BLUE_COLOR = (23, 93, 222)
YELLOW_COLOR = (255, 240, 0)
RED_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (19, 72, 162)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
LIGHT_GRAY_COLOR = (220, 220, 220)
GREEN_COLOR = (0, 255, 0)
DARK_GREEN_COLOR = (0, 100, 0)


class SnakeGameViewer(Observer):
    EXTRA_WIDTH = 0

    def __init__(self, controller: CompetitionController):
        super().__init__(controller)
        self.game_origins = None
        self.pixel_game_width = 0
        self.pixel_game_height = 0

    def reset_games(self):
        board_cols = 2 if len(self.games) >= 4 else 1
        board_rows = math.ceil(len(self.games) / board_cols)

        margin_size = 80  # pixels

        board_row_height = self._screen.get_height() / (board_rows + 1)
        board_col_width = self._screen.get_width() / (board_cols * 2)

        height_ratio = (board_row_height - margin_size) / ARENA_HEIGHT
        width_ratio = (board_col_width - margin_size) / (ARENA_WIDTH + 2 * self.EXTRA_WIDTH)

        self.game_to_pixel_ratio = min(height_ratio, width_ratio)

        self.pixel_game_width = round(
            (ARENA_WIDTH + 2 * self.EXTRA_WIDTH) * self.game_to_pixel_ratio
        )
        self.pixel_game_height = round(ARENA_HEIGHT * self.game_to_pixel_ratio)

        self.game_origins = self.get_origins((self.pixel_game_width, self.pixel_game_height))
        self._font = pygame.font.SysFont("arial", round(36))
        self.draw_all_games()

    def get_game_origin(self, game: SnakeGame) -> Tuple[int, int]:
        assert self.game_origins is not None
        return self.game_origins[self.games.index(game)]

    def get_origins(self, game_dims: Tuple[float, float]) -> Dict[int, Tuple[int, int]]:
        # Figure out the number of columns and rows of games
        game_cols = 2 if len(self.games) >= 4 else 1
        game_rows = math.ceil(len(self.games) / game_cols)

        board_row_height = self._screen.get_height() / (game_rows + 1)
        board_col_width = self._screen.get_width() / (game_cols * 2)

        origins = {}
        for count, game in enumerate(self.games):
            x_origin = board_col_width - game_dims[0] / 2
            x_origin += (
                (count % game_cols) * 2 * board_col_width
            )  # If 2 rows: if odd - right col. If even - left col
            y_origin = board_row_height - game_dims[1] / 2
            y_origin += (
                count // game_cols
            ) * board_row_height  # If odd, bottom row, if even, top row
            origins[count] = (round(x_origin), round(y_origin))

        return origins

    def draw_game(self, game: SnakeGame):
        """Draws match game on screen.

        Args:
            game: The game to draw
        """
        origin = self.get_game_origin(game)

        # Draw background of the board
        pygame.gfxdraw.box(
            self._screen,
            pygame.Rect(
                origin[0],
                origin[1],
                self.pixel_game_width,
                self.pixel_game_height,
            ),
            WHITE_COLOR,
        )

        # Draw apple
        food_screen_x, food_screen_y = game.food_position
        food_screen_y = ARENA_HEIGHT - food_screen_y - 1
        pygame.draw.rect(
            self._screen,
            GREEN_COLOR,
            [
                origin[0] + food_screen_x * self.game_to_pixel_ratio,
                origin[1] + food_screen_y * self.game_to_pixel_ratio,
                self.game_to_pixel_ratio,
                self.game_to_pixel_ratio,
            ],
        )

        # Draw snake body
        for snake_pos in game.snake_body:
            # Flip y axis because pygame counts 0,0 as top left
            snake_y = ARENA_HEIGHT - snake_pos[1] - 1
            pygame.draw.rect(
                self._screen,
                BLACK_COLOR,
                [
                    origin[0] + snake_pos[0] * self.game_to_pixel_ratio,
                    origin[1] + snake_y * self.game_to_pixel_ratio,
                    self.game_to_pixel_ratio + 1,
                    self.game_to_pixel_ratio + 1,
                ],
            )
        # Draw snake head
        snake_y = (
            ARENA_HEIGHT - game.snake_head[1] - 1
        )  # Flip y axis because pygame counts 0,0 as top left
        pygame.draw.rect(
            self._screen,
            DARK_GREEN_COLOR,
            [
                origin[0] + game.snake_head[0] * self.game_to_pixel_ratio,
                origin[1] + snake_y * self.game_to_pixel_ratio,
                self.game_to_pixel_ratio + 1,
                self.game_to_pixel_ratio + 1,
            ],
        )

        # Draw the team name above each game
        img = self._font.render(game.teams[0].name, True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] + self.pixel_game_width // 2,
            origin[1] - self._font.get_height() // 2 - 10,
        )
        self._screen.blit(img, rect)

        # Draw the score
        img = self._font.render(str(game.score), True, BLACK_COLOR, None)
        rect = img.get_rect()
        rect.center = (
            origin[0] - self._font.get_height() // 2,
            origin[1] + self._font.get_height() // 2,
        )
        self._screen.blit(img, rect)

        # Draw the number of steps remaining
        if not game.completed:
            img = self._font.render(
                f"Steps remaining: {game.steps_remaining}", True, BLACK_COLOR, None
            )
            rect = img.get_rect()
            rect.center = (self._screen.get_width() // 2, 50)
            self._screen.blit(img, rect)

    def draw_win_message(self, game: SnakeGame):
        """Displays win message on top of the board."""
        img = self._font.render("Game Over!", True, BLUE_COLOR, None)

        rect = img.get_rect()
        origin = self.get_game_origin(game)
        rect.center = (
            origin[0] + (self.pixel_game_width) // 2,
            origin[1] + (self.pixel_game_height) // 2,
        )

        self._screen.blit(img, rect)
