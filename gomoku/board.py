import numpy as np
import sys

from gomoku.util import NUM_REQUIRED, DIRECTIONS
from gomoku.util import Side

class GomokuBoard:
    def __init__(self, size: int):
        if size < NUM_REQUIRED:
            print(f'Invalid size: {size}')
            sys.exit()
        self.__size = size
        self.reset()

    def reset(self):
        self.__board = np.zeros((self.__size, self.__size), np.int8)
        self.__init_blocked_boards()

    def __init_blocked_boards(self):
        # 4xNxN array keeping track of combinations that have been blocked
        # when this is all True no side can win and the game is a tie
        self.__blocked_black = np.zeros((4, self.__size, self.__size), bool)
        self.__blocked_white = np.zeros((4, self.__size, self.__size), bool)

        # first eliminate combinations that are invalid to start with
        for row in range(self.__size):
            for col in range(self.__size):
                for dir_idx, direction in enumerate(DIRECTIONS):
                    base = np.array([col, row]) + direction * (NUM_REQUIRED - 1)
                    if not self.is_on_board(base):
                        self.__blocked_black[dir_idx, row, col] = True
                        self.__blocked_white[dir_idx, row, col] = True

    def get_board(self) -> np.array:
        return self.__board

    def get_size(self) -> int:
        return self.__size

    def add_piece(self, coord: np.array, side: Side) -> bool:
        assert side.is_player()

        if not self.is_on_board(coord) or self.get_piece(coord).is_player():
            print(f'Invalid coordinate: {coord}')
            return False

        # place piece on board
        print(f'Placing {side} at {coord}')
        self.__board[coord[1], coord[0]] = side.value
        print(self)

        # update blocked boards
        for dir_idx, direction in enumerate(DIRECTIONS):
            for offset in range(NUM_REQUIRED):
                base = np.array(coord) - direction * offset
                if self.is_on_board(base):
                    if side == Side.BLACK:
                        self.__blocked_black[dir_idx, base[1], base[0]] = True
                    else:
                        self.__blocked_white[dir_idx, base[1], base[0]] = True
        return True

    def is_on_board(self, coord: np.array) -> bool:
        return coord[0] >= 0 and coord[0] < self.__size \
            and coord[1] >= 0 and coord[1] < self.__size

    def get_piece(self, coord: np.array) -> Side:
        if not self.is_on_board(coord):
            return Side.NONE
        result = Side(self.__board[coord[1], coord[0]])
        assert result.is_piece()
        return result

    def check_win(self, coord: np.array, side: Side) -> bool:
        assert side.is_player()

        for direction in DIRECTIONS:
            piece_count = 0
            for offset in range(-NUM_REQUIRED+1, NUM_REQUIRED):
                if self.get_piece(coord + direction * offset) == side:
                    piece_count += 1
                    if piece_count == NUM_REQUIRED:
                        return True
                else:
                    piece_count = 0
        return False

    def check_tie(self) -> bool:
        return np.all(self.__blocked_black) and np.all(self.__blocked_white)

    def __repr__(self) -> str:
        return str(self.__board)