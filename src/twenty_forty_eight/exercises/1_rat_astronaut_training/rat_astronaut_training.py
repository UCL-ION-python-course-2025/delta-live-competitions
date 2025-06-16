import numpy as np

import replit

replit.clear()


def room_after_upsidedown_gravity(room):
    """WRITE YOUR CODE HERE.

    Arguments:
        room: a numpy array with random dimensions between 5-10 for both rows and columns.

    Returns:
        gravity_room: a numpy array with the same shape as room, but with the objects moved to the top rows as if gravity were acting on them
    """
    gravity_room = room.copy()

    # Currently you're predicting the pre-gravity and upside-down gravity room to be the same, improve on this!
    return gravity_room


####### DON'T EDIT BELOW HERE #######


def run_tests(board_check, gravity_room):
    assert (
        type(board_check) == np.ndarray
    ), f"UHOH, you outputted a {type(board_check)}.\n\nBut, as a rat, you can only understand numpy arrays!\n\nConvert the output to a rat readable numpy array."

    if not np.array_equal(board_check, gravity_room):
        print(
            "\n Looks like you missed it this time. Your room didn't match the gravity room.\n\nHere's your room:"
        )
        print(board_check)
        for row in board_check:
            print(row)
        print("\n Here's the correct answer:")
        for row in gravity_room:
            print(row)

    if np.shape(board_check) != np.shape(gravity_room):
        print("HINT: Looks like your output takes the wrong shape")
        if np.shape(board_check)[0] != np.shape(gravity_room)[0]:
            print(
                f"It looks like you have the wrong number of rows! Expected {gravity_room.shape[0]} got {board_check.shape[0]}"
            )
        if np.shape(board_check)[1] != np.shape(gravity_room)[1]:
            print(
                f"It looks like you have the wrong number of columns! Expected {gravity_room.shape[1]}, got {board_check.shape[1]}"
            )

    if np.array_equal(board_check, gravity_room):
        return 1

    else:
        return 0


initial_test_rooms = np.asarray(
    [
        np.asarray(
            [
                [0, 0, 0, 1, 0],
                [2, 0, 0, 0, 3],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 5, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 4, 0],
            ]
        ),
        np.asarray(
            [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 6, 0],
                [0, 0, 5, 0, 0, 0],
                [0, 0, 0, 3, 0, 0],
                [1, 0, 2, 0, 0, 0],
                [0, 0, 0, 4, 0, 0],
            ]
        ),
        np.asarray(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 5, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 2, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 4, 0, 3, 0, 0],
            ]
        ),
        np.asarray(
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 4, 5],
                [0, 0, 0, 0, 0],
                [0, 6, 0, 0, 0],
                [0, 0, 0, 0, 1],
                [0, 7, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [2, 0, 0, 0, 0],
                [0, 0, 3, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        ),
        np.asarray(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 3, 0, 0, 0, 0, 0],
                [9, 0, 0, 4, 0, 0, 0, 6, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 7, 0, 8],
                [0, 5, 0, 0, 0, 0, 0, 0, 0],
            ]
        ),
    ],
    dtype=object,
)

final_test_rooms = np.asarray(
    [
        np.asarray(
            [
                [2, 5, 0, 1, 3],
                [0, 0, 0, 4, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        ),
        np.asarray(
            [
                [1, 0, 5, 3, 6, 0],
                [0, 0, 2, 4, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ]
        ),
        np.asarray(
            [
                [0, 2, 0, 5, 0, 3, 0, 1],
                [0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        ),
        np.asarray(
            [
                [2, 6, 3, 4, 5],
                [0, 7, 0, 0, 1],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        ),
        np.asarray(
            [
                [9, 1, 0, 3, 0, 0, 7, 6, 8],
                [0, 2, 0, 4, 0, 0, 0, 0, 0],
                [0, 5, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        ),
    ],
    dtype=object,
)

n_correct = 0

for i, answer in enumerate(final_test_rooms):
    check = room_after_upsidedown_gravity(initial_test_rooms[i])
    n_correct += run_tests(check, final_test_rooms[i])

print(f"You passed {n_correct} tests")
if n_correct < 5:
    print("\nMission failed! Keep going, you will get there!")
if n_correct == 5:
    print("\nMISSION SUCCESS!! Nice work, space rat. See you on Mars.")
