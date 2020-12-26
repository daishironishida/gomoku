import numpy as np

from .base import BaseAgent

class GreedyAgent(BaseAgent):
    __NUM_REQUIRED = 5
    __DIRECTIONS = np.array([[1,0], [1,1], [0,1], [-1,1]])

    def __init__(self, side):
        self.__side = side

    def move(self, board):
        # value is separated into two parts:
        # rightmost 5 bits: indicates offsets at which piece was found
        # value divided by 64: number of pieces found
        combinations = np.zeros((4,) + board.get_board().shape, np.int)

        for row in range(board.get_size()):
            for col in range(board.get_size()):
                for dir_idx, direction in enumerate(self.__DIRECTIONS):
                    for offset in range(self.__NUM_REQUIRED):
                        base = np.array([col, row]) + direction * offset
                        if board.get_piece(base) == self.__side:
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
                        coord = np.array([col, row]) + offset * self.__DIRECTIONS[dir]
                        if board.is_on_board(coord):
                            return coord

        # fallback: should not reach
        print('Fallback: return random value')
        return np.random.randint(0, board.get_size(), 2)