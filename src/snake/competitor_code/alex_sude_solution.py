import random
from typing import List, Tuple

from game_mechanics import ARENA_HEIGHT, ARENA_WIDTH, Action, Orientation, play_snake


def find_orientation(action, snake_direction):
    orientations = [Orientation.SOUTH, Orientation.EAST, Orientation.NORTH, Orientation.WEST]
    if action == Action.MOVE_FORWARD:
        new_orientation = snake_direction
    elif action == Action.TURN_LEFT:
        new_orientation = orientations[(orientations.index(snake_direction) + 1) % 4]
    elif action == Action.TURN_RIGHT:
        new_orientation = orientations[orientations.index(snake_direction) - 1]
    return new_orientation


def find_moves(snake_position, snake_direction):
    actions = [Action.MOVE_FORWARD, Action.TURN_LEFT, Action.TURN_RIGHT]
    available_moves = []
    for action in actions:
        new_orientation = find_orientation(action, snake_direction)
        l = list(snake_position[0])
        if new_orientation == Orientation.SOUTH:
            l[1] = l[1] - 1
        elif new_orientation == Orientation.EAST:
            l[0] = l[0] + 1
        elif new_orientation == Orientation.NORTH:
            l[1] = l[1] + 1
        elif new_orientation == Orientation.WEST:
            l[0] = l[0] - 1
        new_position = tuple(l)
        if (
            new_position not in snake_position[1:]
            and 0 <= new_position[0] < ARENA_WIDTH
            and 0 <= new_position[1] < ARENA_HEIGHT
        ):
            available_moves.append(action)
    return available_moves


def choose_move(
    snake_position: List[Tuple[int, int]],
    snake_direction: Orientation,
    food_position: Tuple[int, int],
) -> Action:
    """THE FUNCTION YOU WRITE.

    Args:
        snake_position: 1st (x, y) is head of the snake, remainder is the body of the snake
    """
    head = snake_position[0]
    food_direction = []
    if food_position[0] > head[0]:
        food_direction.append(Orientation.EAST)
    elif food_position[0] < head[0]:
        food_direction.append(Orientation.WEST)
    if food_position[1] > head[1]:
        food_direction.append(Orientation.NORTH)
    elif food_position[1] < head[1]:
        food_direction.append(Orientation.SOUTH)

    available_moves = find_moves(snake_position, snake_direction)
    if snake_direction == food_direction[0]:
        return Action.MOVE_FORWARD
    elif find_orientation(Action.TURN_LEFT, snake_direction) == food_direction[0]:
        return Action.TURN_LEFT
    elif find_orientation(Action.TURN_RIGHT, snake_direction) == food_direction[0]:
        return Action.TURN_RIGHT
    else:
        return random.choice([Action.MOVE_FORWARD, Action.TURN_LEFT, Action.TURN_RIGHT])


play_snake(choose_move, 1)
