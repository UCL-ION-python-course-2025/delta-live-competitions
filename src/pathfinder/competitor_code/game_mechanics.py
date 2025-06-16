import enum
from time import sleep

import numpy as np


def play_pathfinder(board, choose_move):
    assert isinstance(board, np.ndarray), "`board` has not been loaded as a numpy array."
    assert board.shape == (10, 10), f"`board` has shape {board.shape}"

    position = [np.where(board[:, 0] != 0)[0][0], 0]
    goal = [np.where(board[:, -1] != 0)[0][0], 9]

    print("Here is original path:", board, "\n")

    number_of_path_steps = np.count_nonzero(board == 1)
    count = 1

    while True:
        count += 1

        old_position = position.copy()
        move = choose_move(board, position)
        assert isinstance(move, tuple), "Output move is not a tuple!"
        assert (
            len(move) == 2
        ), f"Dimensions of the move you output are wrong! Should be a 2-dimensional tuple, is a {len(move)}-dimensional tuple"
        position = [position[0] + move[0], position[1] + move[1]]
        board[old_position[0]][old_position[1]] = 2

        board_copy = board.copy()
        board_copy[position[0], position[1]] = 3
        print("\n", board_copy)

        if position == goal:
            board[position[0]][position[1]] = 2
            print("You won!!")
            break

        if position[0] < 0:
            print(f"Here is the path you took:\n{board}\nYou went outside the arena! Game over...")
            break

        if position[0] > len(board):
            print(f"Here is the path you took:\n{board}\nYou went outside the arena! Game over...")
            break

        if position[1] < 0:
            print(f"Here is the path you took:\n{board}\nYou went outside the arena! Game over...")
            break

        if position[1] > len(board):
            print(f"Here is the path you took:\n{board}\nYou went outside the arena! Game over...")
            break
        sleep(1)

    score = (number_of_path_steps - np.count_nonzero(board == 1)) * 100 / count

    print("Game complete!\nYou scored:", score)
    generate_new_board(10, 10)


def count_adjacent_1s(board, position):
    """Go through the next possible moves on adjacent squares and count how many 1's there are."""
    adjacent_positions = get_next_positions(position)
    count = 0
    for p in adjacent_positions:
        pos = adjacent_positions[p]
        if 0 > pos[0] > len(board[0]) - 1:
            continue

        elif 0 > pos[1] > len(board) - 1:
            continue

        try:
            if board[pos[0]][pos[1]] == 1:
                count += 1
        except:
            pass

    return count


def generate_new_board(num_rows: int = 10, num_cols: int = 10) -> np.ndarray:
    """Function to produce a new board with a random path through it.

    Output takes the form of the starting location, the board of 0's and 1's forming a path, and the
    final goal location.
    """

    board = np.zeros((num_rows, num_cols))

    start = int(np.random.choice(np.linspace(1, num_cols - 1, num_cols - 1)))
    generator_position = [start, 0]

    while generator_position[1] < num_rows:
        board[start][0] = 1
        next_positions = get_next_positions(generator_position)
        possible_moves = []

        for p in next_positions:
            pos = next_positions[p]
            if (
                0 < pos[0] < num_cols
                and 0 < pos[1] < num_rows
                and board[pos[0]][pos[1]] != 1
                and count_adjacent_1s(board, pos) <= 1
            ):
                possible_moves.append(pos)

        if generator_position[1] == num_cols - 1:
            board[generator_position[0]][generator_position[1]] = 1
            np.savetxt("board.csv", board, delimiter=",")
            return board

        if possible_moves:
            ind = np.random.choice(np.arange(len(possible_moves)))
            move = possible_moves[ind]
            print(move)
            board[move[0]][move[1]] = 1
            generator_position = move

        else:
            board = np.zeros((num_rows, num_cols))
            generator_position = [start, 0]

    np.savetxt("board.csv", board, delimiter=",")
    return board


def get_next_positions(position):
    moves = {"N": [0, 1], "S": [0, -1], "E": [1, 0], "W": [-1, 0]}
    return {m: [int(position[0] + moves[m][0]), int(position[1] + moves[m][1])] for m in moves}
