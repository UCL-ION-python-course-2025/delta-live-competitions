# 2048
2048 is a simple, but tricky and addictive game. Play it here: https://play2048.co/.

2048 is played on a 4×4 grid, with numbered tiles that all slide together when the player moves them Up, Down, Left or Right.

Every turn, a new tile randomly appears in an empty spot on the board with a value of either 2 or 4.

Tiles slide as far as possible in the chosen direction until they are stopped by either another tile or the edge of the grid. If two tiles of the same number collide while moving, they will merge into a tile with the total value of the two tiles that collided.

The resulting tile cannot merge with another tile again in the same move.

If a move causes three consecutive tiles of the same value to slide together, only the two tiles farthest along the direction of motion will combine.

If all four spaces in a row or column are filled with tiles of the same value, a move parallel to that row/column will combine the first two and last two.

The players score starts at zero, and is increased whenever two tiles combine, by the value of the new tile.

The game ends when the player as no remaining legal moves. This occurs when, there are no empty spaces and no adjacent tiles with the same value.

The goal of the game is to create a 2048 tile. However the game will continue and the player's score will increase until no legal moves remain.



**Your task is to code an AI that plays 2048**

![](/Screenshot.png
)

### 🏆Competition

HOW DO WE RUN THIS?


- At the end, you guessed it, we have a final knockout competition.
- Points you get will be added to the leaderboard
    - **Winners**: 15 points
    - **Runners-up**: 12 points
    - **3rd**: 9 points
    - **Plate winner** (if you lose 1st match but win all others): 7 points
    - **Submit code that works**: 5 points
    - **Don't submit/errors**: 0 points

If your code errors or gives an invalid output, then a random movement will be picked for your turn.

## Technical details

You will need to implement the choose_move function in your main.py file which defines the move that should be played for a given board.

The input to your function is "grid", a 4x4 numpy array containing integers in the position of the board tiles.

You should return one of the following Actions:

- Action.UP
- Action.DOWN
- Action.LEFT
- Action.RIGHT

The tiles will be moved in this direction and your function run again until no more moves are possible and which point you will recieve your score.
