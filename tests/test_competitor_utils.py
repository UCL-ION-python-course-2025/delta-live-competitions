import numpy as np
import pytest

from delta_connect4.game_mechanics import (
    get_empty_board,
    get_piece_longest_line_length,
    has_won,
    is_column_full,
    place_piece,
)


def test_get_empty_board():
    assert get_empty_board().shape == (6, 8)
    assert get_empty_board(1, 2).shape == (1, 2)
    assert np.all(get_empty_board() == 0)


def test_has_won():
    board = np.array(
        [
            [1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    assert not has_won(board, 0)

    board = np.array(
        [
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    assert not has_won(board, 0)

    board = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0],
        ]
    )
    assert has_won(board, 3)

    board = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    assert has_won(board, 3)

    board = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    assert has_won(board, 0)


def test_is_column_full():
    board = get_empty_board(6, 8)
    board[:, 0] = 1
    assert is_column_full(board, 0)
    assert not is_column_full(board, 1)
    assert not is_column_full(board, 2)
    board[:, 3] = -1
    assert is_column_full(board, 3)
    assert not is_column_full(board, 4)
    assert not is_column_full(board, 5)


def test_place_piece():
    board = get_empty_board(6, 8)
    place_piece(board, 0, 1)
    assert board[5, 0] == 1
    place_piece(board, 0, -1)
    assert board[5, 0] == 1
    assert board[4, 0] == -1
    place_piece(board, 1, 1)
    assert board[5, 0] == 1
    assert board[4, 0] == -1
    assert board[5, 1] == 1


def test_get_longest_row():
    board = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    assert get_piece_longest_line_length(board, (5, 0)) == 4

    board = np.array(
        [
            [0, 0, 0, 0, 0, -1, 0, 0],
            [0, 0, 0, 0, -1, 0, 0, 0],
            [0, 0, 0, -1, 0, 0, 0, 0],
            [0, 0, -1, 0, 0, 0, 0, 0],
            [0, -1, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0, 0],
        ]
    )
    assert get_piece_longest_line_length(board, (5, 0)) == 6
