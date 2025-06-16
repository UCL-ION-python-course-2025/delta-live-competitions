import numpy as np

import replit

replit.clear()


def room_after_gravity_merge(room):
    """WRITE YOUR CODE HERE.

    Arguments:
        room: a numpy array with random dimensions between 5-10 for both rows and columns.

    Returns:
        gravity_room: a numpy array with the same shape as room, but with the objects
                moved to the bottom rows as if gravity were acting on them, and with any
                2 objects of the same type
    """
    gravity_room = room.copy()

    # Currently you're predicting the pre-gravity and post-gravity-and-merge rooms to be the same, improve on this!

    return gravity_room


#####################################
####### DON'T EDIT BELOW HERE #######
#####################################


def run_tests(board_check, gravity_room):
    assert type(board_check) == np.ndarray, (
        f"UH OHH - you outputted a {type(board_check)}.\n\n"
        f"But, as a rat, you can only understand numpy arrays!\n\n"
        f"Convert the output to a rat readable numpy array."
    )

    if not np.array_equal(board_check, gravity_room):
        print(
            "\nLooks like you missed it this time. Your room didn't match the gravity room."
            "\n\nHere's your room:"
        )
        for row in board_check:
            print(row)
        print("\n Here's the correct answer:")
        for row in gravity_room:
            print(row)

    if np.shape(board_check) != np.shape(gravity_room):
        print("HINT: Looks like your output takes the wrong shape")
        if np.shape(board_check)[0] != np.shape(gravity_room)[0]:
            print(
                f"It looks like you have the wrong number of rows in the room you returned!\n\nExpected {gravity_room.shape[0]}, got {board_check.shape[0]}"
            )
        if np.shape(board_check)[1] != np.shape(gravity_room)[1]:
            print(
                f"It looks like you have the wrong number of columns in the room you've returned!\n\nExpected {gravity_room.shape[1]} got {board_check.shape[1]}"
            )

    return 1 if np.array_equal(board_check, gravity_room) else 0


initial_test_rooms = [
    np.array(
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
    np.array(
        [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 6, 0],
            [0, 0, 5, 0, 0, 0],
            [0, 0, 0, 3, 0, 0],
            [1, 0, 2, 0, 0, 0],
            [1, 0, 0, 4, 0, 0],
        ]
    ),
    np.array(
        [
            [0, 0, 0, 0, 0, 3, 0, 0],
            [0, 0, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [7, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 3, 0, 0],
        ]
    ),
    np.array(
        [
            [2, 0, 0, 0, 0],
            [2, 0, 0, 4, 5],
            [0, 0, 0, 0, 0],
            [0, 6, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 7, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 6, 0, 0, 0],
            [0, 0, 3, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    ),
    np.array(
        [
            [0, 0, 0, 0, 0, 4, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 8, 0],
            [0, 0, 0, 3, 0, 0, 0, 0, 0],
            [9, 0, 0, 4, 0, 4, 0, 6, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 4, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 7, 0, 8],
            [0, 5, 5, 0, 0, 0, 0, 6, 0],
        ]
    ),
]

final_test_rooms = [
    np.array(
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [2, 5, 0, 4, 3],
        ]
    ),
    np.array(
        [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 5, 3, 0, 0],
            [2, 0, 2, 4, 6, 0],
        ]
    ),
    np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 0, 0, 0],
            [7, 2, 0, 4, 0, 6, 0, 1],
        ]
    ),
    np.array(
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 6, 0, 0, 0],
            [4, 7, 0, 0, 5],
            [4, 6, 3, 4, 1],
        ]
    ),
    np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 2, 3, 0, 4, 0, 8, 0],
            [9, 5, 5, 4, 0, 8, 7, 12, 8],
        ]
    ),
]


n_correct = 0
for initial_room, end_room in zip(initial_test_rooms, final_test_rooms):
    predicted_room = room_after_gravity_merge(initial_room)
    correct = run_tests(predicted_room, end_room)
    n_correct += correct
    if not correct:
        break

print(f"You passed {n_correct} tests")
if n_correct < 5:
    print("\nMission failed! Keep going, you will get there!")
if n_correct == 5:
    print("\nMISSION SUCCESS!! Nice work, space rat. See you on Mars.")
