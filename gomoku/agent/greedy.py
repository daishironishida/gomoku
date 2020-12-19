import numpy as np

from .base import BaseAgent

NUM_REQUIRED = 5
DIRECTIONS = np.array([[1,0], [1,1], [0,1], [-1,1]])

def get_greedy_move(board, side):
    """
    Obtain the best greedy move
    (position which would result in the largest number of pieces in a row)

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
        number of pieces in a row after the move
    """

    # value is separated into two parts:
    # rightmost 5 bits: indicates offsets at which piece was found
    # value divided by 64: number of pieces found
    combinations = np.zeros((4,) + board.get_board().shape, np.int)

    for row in range(board.get_size()):
        for col in range(board.get_size()):
            for dir_idx, direction in enumerate(DIRECTIONS):
                for offset in range(NUM_REQUIRED):
                    base = np.array([col, row]) + direction * offset
                    if board.get_piece(base) == side:
                        combinations[dir_idx, row, col] += 32 + (1 << offset)
                    elif not board.is_on_board(base) or board.get_piece(base) > 0:
                        combinations[dir_idx, row, col] = -1
                        break

    max_count = np.amax(combinations//32)
    for count in range(max_count, -1, -1):
        for dir, row, col in zip(*np.where(combinations//32 == count)):
            flags = combinations[dir, row, col] % 32
            for offset in range(5):
                if flags & (1 << offset) == 0:
                    coord = np.array([col, row]) + offset * DIRECTIONS[dir]
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
