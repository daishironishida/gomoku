# Gomoku

## Requirements

Python >= 3.6

## Run

```
python main.py
```

## Training

### csv format

First line contains `n`, the size of the board.

After this, each move consists of three parts. The first line outputs the player and the coordinates of the move. The next `n` lines shows the state of the board after the move. The final line outputs the winner after the move, -1 if tied, and 0 otherwise.

Sample:

```
5           # board is 5 x 5
1,2,2       # player 1 moves to (2,2)
0,0,0,0,0
0,0,0,0,0
0,0,1,0,0
0,0,0,0,0
0,0,0,0,0
0           # no winner
2,2,0       # player 2 moves to (2,0)
0,0,2,0,0
0,0,0,0,0
0,0,1,0,0
0,0,0,0,0
0,0,0,0,0
0           # no winner

.
.
.

1,1,2       # player 1 moves to (1,2)
0,2,2,0,0
0,0,0,0,2
1,1,1,1,1
0,0,0,0,0
2,0,0,0,0
1           # player 1 wins!
```
