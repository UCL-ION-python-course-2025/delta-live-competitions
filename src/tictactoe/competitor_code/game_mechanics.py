import pickle
import random
from enum import Enum
from typing import Callable, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pygame

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

RED = (255, 0, 0)
BG_COLOR = (20, 200, 160)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)


class Cell(Enum):
    EMPTY = " "
    X = "X"
    O = "O"


def flatten_board(board):
    output = []
    for row in board:
        for item in row:
            output.append(1 if item == Cell.X else -1 if item == Cell.O else 0)
    return output


def save_dictionary(dict: Dict, team_name: str) -> None:
    file_name = f"dict_{team_name}.pkl"
    with open(file_name, "wb") as f:
        pickle.dump(dict, f)


def load_dictionary(team_name: str) -> Dict[str, float]:
    file_name = f"dict_{team_name}.pkl"
    with open(file_name, "rb") as f:
        return pickle.load(f)


class TictactoeMechanics:
    def __init__(self, counter: Cell = Cell.X):
        """Currently this lacks some improvements made to wild_tictactoe.

        It uses Cell enum which Caused problems in the tournament, and the user is given a list of
        ints for the board. Who goes first is confusing and the user has to control both players in
        a semi-unclear way.
        """
        self.counter = counter
        self.player_move = random.choice([Cell.X, Cell.O])
        self.done = False
        self.board = [
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
        ]

    def mark_square(self, row: int, col: int, player: Cell):
        self.board[row][col] = player

    def __repr__(self):
        return str(np.array([x.value for xs in self.board for x in xs]).reshape((3, 3))) + "\n"

    def is_board_full(self):
        """Check if the board is full by checking for empty cells after flattening board."""
        return all(c != Cell.EMPTY for c in [i for sublist in self.board for i in sublist])

    def update(self, move: Tuple[int, int], piece: Cell):
        self.mark_square(move[0], move[1], piece)

    def _check_winning_set(self, iterable: Iterable[Cell]) -> bool:
        unique_pieces = set(iterable)
        return Cell.EMPTY not in unique_pieces and len(unique_pieces) == 1

    def _check_winner(self) -> Optional[Cell]:
        # Check rows
        for row in self.board:
            if self._check_winning_set(row):
                return row[0]

        # Check columns
        for column in [*zip(*self.board)]:
            if self._check_winning_set(column):
                return column[0]

        # Check major diagonal
        size = len(self.board)
        major_diagonal = [self.board[i][i] for i in range(size)]
        if self._check_winning_set(major_diagonal):
            return major_diagonal[0]

        # Check minor diagonal
        minor_diagonal = [self.board[i][size - i - 1] for i in range(size)]
        if self._check_winning_set(minor_diagonal):
            return minor_diagonal[0]

        return None

    def switch_player(self) -> None:
        self.player_move = Cell.X if self.player_move == Cell.O else Cell.O

    def step(
        self, action: int, verbose: bool = False
    ) -> Tuple[List[Cell], Optional[float], bool, Dict]:

        assert not self.done, "Game is done. Call reset() before taking further steps."

        row, col = convert_to_indices(action)
        assert (
            self.board[row][col] == Cell.EMPTY
        ), "You moved onto a square that already has a counter on it!"

        self.mark_square(row, col, self.player_move)
        if verbose:
            print(self)

        winner = self._check_winner()
        reward: Optional[float] = None  # fucking mypy

        if winner is not None:
            self.done = True
            reward = 1.0 if winner == self.counter else 0.0
            if verbose:
                print(f"{self.player_move.value} wins!")
        elif self.is_board_full():
            self.done = True
            reward = 0.0
            if verbose:
                print("Game Drawn")

        self.switch_player()
        info = {"player_move": self.player_move if not self.done else None, "winner": winner}

        return flatten_board(self.board), reward, self.done, info

    def reset(self) -> Tuple[List[Cell], Optional[float], bool, Dict]:
        self.board = [
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
        ]

        self.player_move = random.choice([Cell.X, Cell.O])
        self.done = False
        return flatten_board(self.board), None, self.done, {"player_move": self.player_move}


def draw_non_board_elements(screen, game):
    draw_pieces(screen, game.board)


def draw_pieces(screen, board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == Cell.O:
                pygame.draw.circle(
                    screen,
                    CIRCLE_COLOR,
                    (
                        int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                        int(row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    ),
                    CIRCLE_RADIUS,
                    CIRCLE_WIDTH,
                )
            elif board[row][col] == Cell.X:
                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                    (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                    CROSS_WIDTH,
                )
                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                    (
                        col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                        row * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                    ),
                    CROSS_WIDTH,
                )


def check_and_draw_win(board: List, player: Cell, screen: pygame.Surface) -> bool:
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(screen, col, player)
            return True

    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(screen, row, player)
            return True

    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(screen, player)
        return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(screen, player)
        return True

    return False


def draw_vertical_winning_line(screen, col, player: Cell):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2

    pygame.draw.line(
        screen,
        CIRCLE_COLOR if player == Cell.O else CROSS_COLOR,
        (posX, 15),
        (posX, HEIGHT - 15),
        LINE_WIDTH,
    )


def draw_horizontal_winning_line(screen, row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2

    pygame.draw.line(
        screen,
        CIRCLE_COLOR if player == Cell.O else CROSS_COLOR,
        (15, posY),
        (WIDTH - 15, posY),
        WIN_LINE_WIDTH,
    )


def draw_asc_diagonal(screen, player: Cell):
    pygame.draw.line(
        screen,
        CIRCLE_COLOR if player == Cell.O else CROSS_COLOR,
        (15, HEIGHT - 15),
        (WIDTH - 15, 15),
        WIN_LINE_WIDTH,
    )


def draw_desc_diagonal(screen, player: Cell):
    pygame.draw.line(
        screen,
        CIRCLE_COLOR if player == Cell.O else CROSS_COLOR,
        (15, 15),
        (WIDTH - 15, HEIGHT - 15),
        WIN_LINE_WIDTH,
    )


def convert_to_indices(number: int) -> Tuple[int, int]:
    assert number in range(9), f"Output ({number}) not a valid number from 0 -> 8"
    return number // 3, number % 3


def robot_choose_move(board):
    possible_moves = [tuple(tup) for tup in np.array(np.where(np.array(board) == Cell.EMPTY)).T]

    return possible_moves[np.random.choice(range(len(possible_moves)))]


def render(choose_move: Callable[[List[int], Dict], int], player_dict: Dict):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TIC TAC TOE")
    screen.fill(BG_COLOR)

    # DRAW LINES
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(
        screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH
    )

    game = TictactoeMechanics(Cell.X)

    game_quit = False
    game_over = False
    player_move = random.choice([Cell.X, Cell.O])

    while not game_quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and game_over):
                game_quit = True

            if event.type == pygame.MOUSEBUTTONDOWN and not game_quit:

                if player_move == Cell.X:
                    row, col = convert_to_indices(
                        choose_move(flatten_board(game.board), player_dict)
                    )
                else:
                    # row, col = convert_to_indices(choose_move(flatten_board(game.board)))
                    row, col = robot_choose_move(game.board)

                assert game.board[row][col] == Cell.EMPTY

                game.mark_square(row, col, player_move)
                game_over = check_and_draw_win(game.board, player_move, screen=screen)

                player_move = Cell.O if player_move == Cell.X else Cell.X

                draw_non_board_elements(screen, game)
        pygame.display.update()
