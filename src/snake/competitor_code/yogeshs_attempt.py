import random
from typing import List, Tuple

from .game_mechanics import (
    ARENA_HEIGHT,
    ARENA_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    Action,
    Orientation,
    play_snake,
)


def choose_move(
    snake_position: List[Tuple[int, int]],
    snake_direction: Orientation,
    food_position: Tuple[int, int],
) -> Action:
    print(snake_position)
    print(ARENA_WIDTH, ARENA_HEIGHT)
    print(food_position)
    print(snake_direction)
    print("*************")
    # if snake_position[0][0] + 1 > ARENA_WIDTH and snake_direction:
    #   return random.choice([Action.TURN_LEFT, Action.TURN_RIGHT])
    # elif snake_position[0][1] + 1 > ARENA_HEIGHT or snake_position[0][1]-1 <0:
    #    return random.choice([Action.TURN_LEFT, Action.TURN_RIGHT])

    # aknfsklnfskfnsa,lfnsalf
    if snake_position[0][0] < food_position[0] and snake_direction == Orientation.NORTH:
        return Action.TURN_RIGHT
    elif snake_position[0][0] < food_position[0] and snake_direction == Orientation.SOUTH:
        return Action.TURN_LEFT
    elif snake_position[0][0] < food_position[0] and snake_direction == Orientation.WEST:
        if snake_position[0][1] + 1 > ARENA_HEIGHT and not snake_position[0][1] - 1 < 0:
            return Action.TURN_RIGHT
        else:
            return Action.TURN_LEFT
    elif snake_position[0][0] < food_position[0] and snake_direction == Orientation.EAST:
        # next_x = snake_position[0][0]+1
        # if(item for item in snake_position if next_x in item)
        return Action.MOVE_FORWARD

    elif snake_position[0][0] > food_position[0] and snake_direction == Orientation.NORTH:
        return Action.TURN_LEFT
    elif snake_position[0][0] > food_position[0] and snake_direction == Orientation.SOUTH:
        return Action.TURN_RIGHT
    elif snake_position[0][0] > food_position[0] and snake_direction == Orientation.WEST:
        return Action.MOVE_FORWARD
    elif snake_position[0][0] > food_position[0] and snake_direction == Orientation.EAST:
        if snake_position[0][1] + 1 > ARENA_HEIGHT and not snake_position[0][1] - 1 < 0:
            return Action.TURN_LEFT
        else:
            return Action.TURN_RIGHT

    elif (
        snake_position[0][1] < food_position[1]
        and snake_position[0][0] == food_position[0]
        and snake_direction == Orientation.EAST
    ):
        return Action.TURN_LEFT
    elif (
        snake_position[0][1] < food_position[1]
        and snake_position[0][0] == food_position[0]
        and snake_direction == Orientation.WEST
    ):
        return Action.TURN_RIGHT
    elif (
        snake_position[0][1] < food_position[1]
        and snake_position[0][0] == food_position[0]
        and snake_direction == Orientation.NORTH
    ):
        if snake_position[0][0] + 1 > ARENA_WIDTH and not snake_position[0][0] - 1 < 0:
            return Action.TURN_LEFT
        else:
            return Action.TURN_RIGHT
    elif (
        snake_position[0][1] < food_position[1]
        and snake_position[0][0] == food_position[0]
        and snake_direction == Orientation.SOUTH
    ):
        return Action.MOVE_FORWARD

    elif (
        snake_position[0][1] > food_position[1]
        and snake_position[0][0] == food_position[0]
        and snake_direction == Orientation.EAST
    ):
        return Action.TURN_RIGHT
    elif (
        snake_position[0][1] > food_position[1]
        and snake_position[0][0] == food_position[0]
        and snake_direction == Orientation.WEST
    ):
        return Action.TURN_LEFT
    elif (
        snake_position[0][1] > food_position[1]
        and snake_position[0][0] == food_position[0]
        and snake_direction == Orientation.NORTH
    ):
        return Action.MOVE_FORWARD
    elif (
        snake_position[0][1] > food_position[1]
        and snake_position[0][0] == food_position[0]
        and snake_direction == Orientation.SOUTH
    ):
        if snake_position[0][0] + 1 > ARENA_WIDTH and not snake_position[0][0] - 1 < 0:
            return Action.TURN_RIGHT
        else:
            return Action.TURN_LEFT
    return random.choice([Action.TURN_LEFT, Action.TURN_RIGHT, Action.MOVE_FORWARD])


# play_snake(choose_move, 5)
