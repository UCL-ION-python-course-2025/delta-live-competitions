import random
from typing import List, Tuple

from .game_mechanics import Action, Orientation, play_snake


def choose_move(
    snake_position: List[Tuple[int, int]],
    snake_direction: Orientation,
    food_position: Tuple[int, int],
) -> Action:
    return random.choice([Action.MOVE_FORWARD])
