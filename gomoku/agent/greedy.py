import numpy as np

from .base import BaseAgent

NUM_REQUIRED = 5
DIRECTIONS = np.array([[1,0], [1,1], [0,1], [-1,1]])

def get_greedy_move(board, side):
    """
    Obtain the best greedy move
    (position which would result in the largest number of pieces in a
    five in a row slot)

    Parameters
    ----------
    board : GomokuBoard
        current state of the board
    side : int
        side of the agent

    Returns
    -------
    move: np.array
        best greedy move
    count: int
        number of pieces in the five in a row slot after the move

    Notes
    -----
    Algorithm and implementation details

    First we enumerate all possible five in a row combinations on the board.
    This can be done by considering slots starting at each coordinate,
    in four directions (horizontal, vertical, and two diagonals).

    These slots are represented by a 4xNxN array, where N is the size
    of the board. Each value (i,x,y) represents a slot starting at
    (x,y) going in the ith direction. (Note that some of these slots
    are invalid since parts of the slot go off the board.)

    The value of this array, represented in bits, consists of two parts.

    The rightmost 5 bits are flags which indicate offsets of this slot
    at which a piece was found. For example, a slot such as [_,1,_,_,1]
    would be represented as 10010 for player 1. (Least significant bit is
    the beginning of the slot, most significant is the end.)

    The remaining bits represents the number of agent's pieces in this slot,
    if a combination can still be made, or -1 otherwise. Note that this
    number can be obtained by divinding the value of the array by 32 (2^5).

    The slot [_,1,_,_,1] has 2 pieces for agent 1, so the value of this
    slot would be 2*32 + 0b10010 = 73. The slot [_,1,2,_,1] has value -1,
    since a combination can no longer be made for either agent.

    We then use these values to find the slot where the highest number of
    pieces are already in place, and a combination can still be made.
    We return the coordinate which fills one of the remaining pieces of
    the slot.
    """

    # 4xNxN array enumerating all possible slots on the board
    combinations = np.zeros((4,) + board.get_board().shape, np.int)

    # Traverse the board and calculate value of the array
    for row in range(board.get_size()):
        for col in range(board.get_size()):
            for dir_idx, direction in enumerate(DIRECTIONS):
                for offset in range(NUM_REQUIRED):
                    base = np.array([col, row]) + direction * offset

                    # if agent's piece is found, add 32 and raise flag
                    if board.get_piece(base) == side:
                        combinations[dir_idx, row, col] += 32 + (1 << offset)
                    # if opponent's piece is found, or the slot is invalid,
                    # update value to -1
                    elif not board.is_on_board(base) or board.get_piece(base) > 0:
                        combinations[dir_idx, row, col] = -1
                        break

    # starting with the maximum count, look for possible moves and return the
    # first valid one found
    max_count = np.amax(combinations//32)
    for count in range(max_count, -1, -1):
        for dir, row, col in zip(*np.where(combinations//32 == count)):
            flags = combinations[dir, row, col] % 32
            for offset in range(5):
                # find a remaining coordinate from the slot
                if flags & (1 << offset) == 0:
                    coord = np.array([col, row]) + offset * DIRECTIONS[dir]
                    # this check may be unnecessary
                    if board.is_on_board(coord):
                        return coord, count+1

    # fallback: should not reach
    print('Fallback: return random value')
    return np.random.randint(0, board.get_size(), 2), 0

class GreedyAgent(BaseAgent):
    def __init__(self, side):
        self.__side = side

    def move(self, board):
        result, _ = get_greedy_move(board, self.__side)
        return result

class GreedyDefendingAgent(BaseAgent):
    def __init__(self, side):
        self.__side = side

    def get_opponent(self):
        if self.__side == 1:
            return 2
        else:
            return 1

    def move(self, board):
        my_result, my_count = get_greedy_move(board, self.__side)
        opponent_result, opponent_count = get_greedy_move(board, self.get_opponent())

        # if agent is closer to winning, make an attacking move
        if my_count >= opponent_count:
            return my_result
        # if opponent is closer to winning, make a defending move
        else:
            return opponent_result
