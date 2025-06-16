import os
import time
from typing import Any, List, Optional, Tuple

import numpy as np
import pygame
from pygame.surface import Surface

from visual_utils import wrap_text

WIDTH, HEIGHT = 633, 900

GREEN = "#6aaa64"
YELLOW = "#c9b458"
GREY = "#787c7e"
OUTLINE = "#d3d6da"
FILLED_OUTLINE = "#878a8c"


ASSET_PATH = os.path.join(os.path.dirname(__file__), "assets")
COLOR_MAP = {2: GREEN, 1: YELLOW, 0: GREY}


def create_text(
    screen: Surface,
    text: str,
    color: Tuple[int, int, int],
    pos: Tuple[int, int],
    font: pygame.font.Font,
    max_width=None,
    background_color: Optional[Tuple[int, int, int]] = None,
) -> None:

    assert screen is not None

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
        screen.blit(*text_object)


class WorldleVisualisationController:
    def __init__(self, team_name: str, game_speed_multipler: float) -> None:
        """Worldle visualisation single game."""
        self.game_speed_multipler = game_speed_multipler
        self.guess_count = 0
        self.team_name = team_name

    def draw_standalone_game(self) -> None:
        self.set_starting_position(110.0, 12.0)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.draw_game(screen, scale=1)

    def set_starting_position(self, x_pos: float, y_pos: float) -> None:
        self.x_starting_pos = x_pos
        self.y_starting_pos = y_pos

    def reset(self) -> None:
        self.guess_count = 0

    def draw_game(self, screen: Surface, scale: float) -> None:

        self.screen = screen

        self.letter_x_spacing = 85 * scale
        self.letter_y_spacing = 12 * scale
        self.letter_size = 75 * scale
        pygame.font.init()
        self.guessed_letter_font = pygame.font.Font(
            os.path.join(ASSET_PATH, "FreeSansBold.otf"), int(50 * scale)
        )
        self.top_text_font = pygame.font.Font(
            os.path.join(ASSET_PATH, "FreeSansBold.otf"), int(30 * scale)
        )
        self.bottom_text_font = pygame.font.Font(
            os.path.join(ASSET_PATH, "FreeSansBold.otf"), int(40 * scale)
        )

        self.side_text_font = pygame.font.Font(
            os.path.join(ASSET_PATH, "FreeSansBold.otf"), int(25 * scale)
        )
        self.scale = scale
        self.draw_outline()

    def display_score(self, rounds_solved: int, n_guesses: int) -> None:
        create_text(
            self.screen,
            f"Rounds Solved: {rounds_solved}. Guesses: {n_guesses}",
            color=(1, 1, 1),
            pos=(
                int(self.x_starting_pos - 1.1 * self.letter_size),
                int(self.y_starting_pos + 3 * self.letter_size),
            ),
            font=self.side_text_font,
            max_width=5,
        )

    def draw_outline(self) -> None:
        y_pos = self.y_starting_pos
        x_pos = self.x_starting_pos
        for y in range(1, 7):
            for x in range(5):
                new_letter = Letter(
                    self.screen,
                    (x_pos, y_pos),
                    "",
                    "white",
                    self.guessed_letter_font,
                    self.letter_size,
                    scale=self.scale,
                )
                new_letter.draw()
                x_pos += self.letter_x_spacing

            y_pos = y * 100 * self.scale + self.y_starting_pos
            x_pos = self.x_starting_pos

    def display_word(self, word: str, result: List[int]) -> None:
        # y_pos = self.guess_count * 100 + self.y_starting_pos
        y_pos = self.guess_count * 100 * self.scale + self.y_starting_pos
        x_pos = self.x_starting_pos
        colors = [COLOR_MAP[res] for res in result]

        for letter, color in zip(word, colors):
            new_letter = Letter(
                self.screen,
                (x_pos, y_pos),
                letter,
                color,
                self.guessed_letter_font,
                self.letter_size,
                scale=self.scale,
            )
            new_letter.draw()
            x_pos += self.letter_x_spacing
            time.sleep(0.5 / self.game_speed_multipler)

        x_pos = self.x_starting_pos
        self.guess_count += 1

    def display_game_over_text(self, n_guesses_allowed: int, correct_word: str) -> None:
        self.display_bottom_text("Word Not Found!", color="red")

    def display_winning_text(self, n_guesses: int, word: str) -> None:
        self.display_bottom_text("Word Found!", color=GREEN)

    def display_bottom_text(
        self, txt: str, offset: int = 0, color: str = "black"
    ) -> None:
        text = self.bottom_text_font.render(txt, True, color)
        play_again_rect = text.get_rect(
            center=(
                self.x_starting_pos + 3 * self.letter_size,
                self.y_starting_pos + 8 * self.letter_size + offset,
            )
        )
        self.screen.blit(text, play_again_rect)
        pygame.display.update()

    def display_team_name(self) -> None:
        self.display_top_text(self.team_name)

    def display_top_text(self, txt: str) -> None:
        text = self.bottom_text_font.render(txt, True, "black")
        top_rect = text.get_rect(
            center=(
                self.x_starting_pos + 3 * self.letter_size,
                self.y_starting_pos - 0.4 * self.letter_size,
            )
        )
        self.screen.blit(text, top_rect)
        pygame.display.update()


class Letter:
    def __init__(
        self,
        screen: Surface,
        position: Tuple[float, float],
        text: str,
        background_color: str,
        font: Any,
        size: float = 75,
        scale: float = 1,
    ):
        # Initializes all the variables, including text, color, position, size, etc.
        self.background_color = background_color
        self.text_color = "black"
        self.position = position
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.background_rect = (position[0], self.y_pos, size, size)
        self.text = text
        self.text_position = (self.x_pos + 36 * scale, self.position[1] + 34 * scale)
        self.text_surface = font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)
        self.screen = screen
        self.font = font

    def draw(self) -> None:
        # Puts the letter and text on the screen at the desired positions.
        pygame.draw.rect(self.screen, self.background_color, self.background_rect)
        if self.background_color == "white":
            pygame.draw.rect(self.screen, FILLED_OUTLINE, self.background_rect, 3)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.screen.blit(self.text_surface, self.text_rect)
        pygame.display.update()
