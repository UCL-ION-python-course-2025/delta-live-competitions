import random
from typing import Callable, Tuple

import numpy as np

from game_parent import PointsGame
from pathfinder.competitor_code.game_mechanics import generate_new_board
from pathfinder.competitor_code.robot import choose_move
from team import Team


class PathfinderMechanics:
    def __init__(self):
        self.board = generate_new_board(10, 10)
        self.position = (np.where(self.board[:, 0] != 0)[0][0], 0)
        self.goal = (np.where(self.board[:, -1] != 0)[0][0], 9)
        self.orig_path_length = np.count_nonzero(self.board == 1)
        self.num_steps_taken = (
            1  # Yes this is broken but it's how Matt left it and I presume changing will break it
        )

    def reset(self):
        self.board = generate_new_board(10, 10)
        self.position = (np.where(self.board[:, 0] != 0)[0][0], 0)
        self.goal = (np.where(self.board[:, -1] != 0)[0][0], 9)
        self.orig_path_length = np.count_nonzero(self.board == 1)
        self.num_steps_taken = (
            1  # Yes this is broken but it's how Matt left it and I presume changing will break it
        )

    def update(
        self,
        choose_move: Callable[[np.ndarray, Tuple[int, int]], Tuple[int, int]],
    ):
        try:
            move = choose_move(self.board, self.position)
            assert isinstance(move, tuple), "Output move is not a tuple!"
            assert len(move) == 2, (
                f"Dimensions of the move you output are wrong!\n\n"
                f"Should be a 2-dimensional tuple, but is a {len(move)}-dimensional tuple"
            )
            assert move in [(0, 1), (0, -1), (1, 0), (-1, 0)]
            assert self.is_position_valid((self.position[0] + move[0], self.position[1] + move[1]))
        except:
            possible_moves = [
                move
                for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]
                if self.is_position_valid((self.position[0] + move[0], self.position[1] + move[1]))
            ]
            move = random.choice(possible_moves)
        # Make previous location 2
        self.board[self.position[0]][self.position[1]] = 2
        self.position = (self.position[0] + move[0], self.position[1] + move[1])

    def is_position_valid(self, position: Tuple[int, int]) -> bool:
        return 0 <= position[0] < len(self.board) and 0 <= position[1] < len(self.board)

    def __repr__(self):
        board_copy = self.board.copy()
        board_copy[self.position[0], self.position[1]] = 3
        print("\n", board_copy)


class PathfinderGame(PointsGame, PathfinderMechanics):
    NAME = "Pathfinder"
    ROBOT_PLAYER = Team("Robot", choose_move)

    def __init__(
        self,
        name: str,
        team: Team,
    ):
        PointsGame.__init__(self, name, team)
        PathfinderMechanics.__init__(self)
        self.max_steps = 100

    def step(self) -> None:
        if self.completed:
            return

        self.num_steps_taken += 1

        self.update(self._team.choose_move)

        if (
            self.steps_remaining == 0
            or self.position == self.goal
            or not self.is_position_valid(self.position)
        ):
            self.score = (
                (self.orig_path_length - np.count_nonzero(self.board == 1) - 1)
                * 100
                / self.num_steps_taken
            )
            self.complete()

    def reset_game(self):
        self.reset()
        super(PathfinderGame, self).reset_game()

    @property
    def steps_remaining(self) -> int:
        return self.max_steps - self.num_steps_taken
