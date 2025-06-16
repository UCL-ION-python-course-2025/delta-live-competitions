import random
from typing import Callable, List, Optional, Tuple

from game_mechanics import ARENA_HEIGHT, ARENA_WIDTH, Action, Orientation, play_snake


def not_dead(new_position: Tuple[int, int], snake_position: List[Tuple[int, int]]) -> bool:
    """Check if the new snake head is not dead.

    It is dead if it leaves the arena or hits itself.
    """
    in_x = 0 <= new_position[0] < ARENA_WIDTH
    in_y = 0 <= new_position[1] < ARENA_HEIGHT
    return new_position not in snake_position[1:-1] and in_x and in_y


def get_next_position(position: Tuple[int, int], direction: Orientation) -> Tuple[int, int]:
    """Get the next position after moving in the given direction."""
    x, y = position
    if direction.value % 2 == 0:
        # South is 0 (y -= 1), North is 2 (y += 1)
        y += direction.value - 1
    else:
        # East is 1 (x += 1), West is 3 (x -= 1)
        x += 2 - direction.value
    return x, y


def get_new_orientation(action: Action, snake_direction: Orientation) -> Orientation:
    """Get the new orientation after the given action."""
    if action.value == Action.MOVE_FORWARD.value:
        new_orientation = snake_direction.value
    elif action.value == Action.TURN_LEFT.value:
        new_orientation = (snake_direction.value + 1) % 4
    else:
        new_orientation = (snake_direction.value - 1) % 4
    return Orientation(new_orientation)


def opposite_dir(direction):
    """Get the opposite direction of the given direction."""
    return Orientation((direction.value + 2) % 4)


def choose_move(
    snake_position: List[Tuple[int, int]],
    snake_direction: Orientation,
    food_position: Tuple[int, int],
) -> Action:
    # Get the possible directions the snake can move in.
    possible_directions = [Orientation(i) for i in range(4)]
    possible_directions.remove(opposite_dir(snake_direction))
    actions = [Action.MOVE_FORWARD, Action.TURN_LEFT, Action.TURN_RIGHT]

    # Figure out the directions the snake SHOULD move in
    directions_to_go = []

    if food_position[0] - snake_position[0][0] > 0:
        directions_to_go.append(Orientation.EAST)
    elif food_position[0] - snake_position[0][0] < 0:
        directions_to_go.append(Orientation.WEST)
    if food_position[1] - snake_position[0][1] < 0:
        directions_to_go.append(Orientation.SOUTH)
    elif food_position[1] - snake_position[0][1] > 0:
        directions_to_go.append(Orientation.NORTH)

    # We want to know which actions don't kill the snake so we can pick between them
    not_dead_actions = []
    for action in actions:
        # For the action, figure out the new direction and position it's in
        new_direction = get_new_orientation(action, snake_direction)
        new_position = get_next_position(snake_position[0], new_direction)

        # Only consider actions that DON'T KILL THE SNAKE!
        if not_dead(new_position, snake_position):
            not_dead_actions.append(action)

            # If an action is one we want to go in and it doesn't kill the snake, take it
            if new_direction in directions_to_go:
                return action

    # If none of the actions are in the direction of the food, we want to pick between actions which don't kill us
    if not_dead_actions:
        return random.choice(not_dead_actions)

    # If there are no options which don't kill us, pick any of them - THIS STOPS US FROM ERRORING!
    return random.choice(actions)


play_snake(choose_move, 1)
