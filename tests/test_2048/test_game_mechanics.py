import random

import numpy as np

from src.twenty_forty_eight.competitor_code import Action, TwentyFortyEight


def test_possible_actions() -> None:
    t = TwentyFortyEight()
    t.board *= 0
    t.board[:, 3] = 2
    assert all(action in t.possible_actions for action in [Action.DOWN, Action.LEFT, Action.UP])

    t.board *= 0
    t.board[3, 0] = 2
    t.board[3, 1] = 4
    t.board[3, 2] = 8
    t.board[3, 3] = 16
    assert t.possible_actions == [Action.UP]

    t.board = np.array(
        [
            [2, 4, 8, 16],
            [4, 8, 16, 2],
            [8, 16, 2, 4],
            [16, 2, 4, 8],
        ]
    )
    assert t.possible_actions == []


def test_tile_locations() -> None:
    t = TwentyFortyEight()
    t.board *= 0
    t.board[:, 3] = 2
    assert all(loc in t.tile_locations for loc in [(0, 3), (1, 3), (2, 3), (3, 3)])

    t.board *= 0
    t.board[3, 0] = 2
    t.board[3, 1] = 4
    t.board[3, 2] = 8
    t.board[3, 3] = 16
    assert np.all(t.tile_locations == np.array([(3, 0), (3, 1), (3, 2), (3, 3)]))

    t.board = np.zeros((4, 4))
    assert len(t.tile_locations) == 0


def test_game_over() -> None:
    t = TwentyFortyEight()
    assert not t.game_over

    t.board = np.array(
        [
            [2, 4, 8, 16],
            [4, 8, 16, 2],
            [8, 16, 2, 4],
            [16, 2, 4, 8],
        ]
    )
    assert t.game_over

    t.board = np.ones((4, 4))
    assert not t.game_over


def test_spawn_new_tile() -> None:
    t = TwentyFortyEight()
    orig_num_tiles = len(t.tile_locations)
    t.spawn_new_tile()
    assert len(t.tile_locations) == orig_num_tiles + 1
    t.spawn_new_tile()
    t.spawn_new_tile()
    t.spawn_new_tile()
    assert len(t.tile_locations) == orig_num_tiles + 4


def test_slide_up() -> None:
    t = TwentyFortyEight()
    t.board *= 0

    # Slide up should have no effect
    t.board[:, 0] = 2
    t.slide_up()
    expected_board = np.zeros((4, 4))
    expected_board[:, 0] = 2
    assert np.all(t.board == expected_board)

    # Same again
    t.board[:, 0] = 4
    t.slide_up()
    expected_board[:, 0] = 4
    assert np.all(t.board == expected_board)

    # 8 should slide to top
    t.board[3, 1] = 8
    t.slide_up()
    expected_board[0, 1] = 8

    assert np.all(t.board == expected_board)


def test_combine_tiles() -> None:
    t = TwentyFortyEight()
    t.board *= 0

    # 2, 0, 0, 0
    # 2, 0, 0, 0
    # 2, 0, 0, 0
    # 2, 0, 0, 0
    t.board[:, 0] = 2
    t.combine_tiles()

    # 4, 0, 0, 0
    # 4, 0, 0, 0
    # 0, 0, 0, 0
    # 0, 0, 0, 0
    expected_board = np.zeros((4, 4))
    expected_board[0, 0] = 4
    expected_board[2, 0] = 4
    assert np.all(t.board == expected_board)


def test_update() -> None:
    t = TwentyFortyEight()
    t.board *= 0

    # 2, 0, 0, 0
    # 2, 0, 0, 0
    # 2, 0, 0, 0
    # 2, 0, 0, 0
    t.board[:, 0] = 2
    t.update(lambda x: Action.UP)

    assert t.board[0, 0] == 4
    assert t.board[1, 0] == 4
    assert len(t.tile_locations) == 3


def test_play_round() -> None:
    t = TwentyFortyEight()
    t.play_round(lambda x: random.choice(t.possible_actions), 10000)

    assert t.game_over
    assert np.all(t.board != 0)
