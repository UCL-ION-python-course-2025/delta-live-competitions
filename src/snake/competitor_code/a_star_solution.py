import random
from typing import Callable, List, Optional, Tuple

from game_mechanics import ARENA_HEIGHT, ARENA_WIDTH, Action, Orientation, play_snake


def get_possible_actions(
    snake_position: List[Tuple[int, int]], snake_direction: Orientation
) -> List[Action]:
    actions = [Action.MOVE_FORWARD, Action.TURN_LEFT, Action.TURN_RIGHT]
    not_dead_actions = []
    for action in actions:
        new_direction = get_new_orientation(action, snake_direction)
        new_position = get_next_position(snake_position[0], new_direction)
        if not_dead(new_position, snake_position):
            not_dead_actions.append(action)
    return not_dead_actions


def l1_dist(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


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


def a_star(
    snake_position: List[Tuple[int, int]],
    snake_direction: Orientation,
    food_position: Tuple[int, int],
    possible_actions: List[Action],
):
    new_orientations = [get_new_orientation(action, snake_direction) for action in possible_actions]
    new_positions = [
        get_next_position(snake_position[0], new_orientation)
        for new_orientation in new_orientations
    ]

    h: Callable[[Tuple[int, int]], int] = lambda pos: l1_dist(pos, food_position)
    closed_list = [Node(snake_position[0], None, h)]
    open_list = [Node(new_pos, closed_list[0], h) for new_pos in new_positions]
    current_node = min(reversed(open_list), key=lambda node: node.f)

    for _ in range(480):
        if not open_list:
            path = current_node.get_path()
            return path

        current_node = min(reversed(open_list), key=lambda node: node.f)

        # If food reached or no more open nodes, return path
        if current_node.position == food_position:
            path = current_node.get_path()
            return path

        open_list.remove(current_node)
        closed_list.append(current_node)

        for pos_change in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_pos = (
                current_node.position[0] + pos_change[0],
                current_node.position[1] + pos_change[1],
            )

            # Skip if parent - that would mean going backwards
            if current_node.parent is not None and next_pos is current_node.parent.position:
                continue
            # Skip if move will kill the snake (back of snake moves -current_node.g steps)
            if not not_dead(next_pos, snake_position[1 : -current_node.g]):
                continue
            # Skip if already in closed list
            if next_pos in [node.position for node in closed_list]:
                continue
            # is it already in open list?
            open_list_node_pos = [node.position for node in open_list]
            if next_pos in open_list_node_pos:
                # if so, check if it is a better path
                next_pos_index = open_list_node_pos.index(next_pos)
                next_pos_node = open_list[next_pos_index]
                if next_pos_node.g > current_node.g + 1:
                    next_pos_node.replace_parent(current_node)
            else:
                # if not, add it to open list
                open_list.append(Node(next_pos, current_node, h))
    return []


class Node:
    def __init__(
        self,
        position: Tuple[int, int],
        parent: Optional["Node"],
        h: Callable[[Tuple[int, int]], int],
    ):
        self.position = position
        self.parent = parent
        self.g: int = parent.g + 1 if parent else 0
        self.h: int = h(position)
        self.f: int = self.g + self.h

    def replace_parent(self, new_parent: "Node"):
        self.parent = new_parent
        self.g = new_parent.g + 1 if new_parent else 0
        self.f = self.g + self.h

    def get_path(self) -> List[Tuple[int, int]]:
        path = []
        current_node = self
        while current_node.parent:
            path.append(current_node.position)
            current_node = current_node.parent
        return path


def choose_move(
    snake_position: List[Tuple[int, int]],
    snake_direction: Orientation,
    food_position: Tuple[int, int],
) -> Action:
    possible_directions = [Orientation(i) for i in range(4)]
    possible_directions.remove(opposite_dir(snake_direction))
    possible_actions = get_possible_actions(snake_position, snake_direction)

    optimal_path = a_star(snake_position, snake_direction, food_position, possible_actions)
    if optimal_path:
        first_step = optimal_path[-1]
        new_directions = [
            get_new_orientation(action, snake_direction) for action in possible_actions
        ]
        new_positions = [
            get_next_position(snake_position[0], new_direction) for new_direction in new_directions
        ]

        best_poss_position = min(
            new_positions, key=lambda new_position: l1_dist(first_step, new_position)
        )
        best_action = possible_actions[new_positions.index(best_poss_position)]
        return best_action
    else:
        if possible_actions:
            return random.choice(possible_actions)
        return random.choice([Action.TURN_LEFT, Action.TURN_RIGHT, Action.MOVE_FORWARD])


play_snake(choose_move, 5)
