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
        self.__board = np.zeros((self.__size, self.__size), np.int8)

    def get_board(self) -> np.array:
        return self.__board

    def get_size(self) -> int:
        return self.__size

    def add_piece(self, coord: np.array, side: Side) -> bool:
        assert side.is_player()

        if not self.is_on_board(coord) or self.get_piece(coord).is_player():
            print(f'Invalid coordinate: {coord}')
            return False

        print(f'Placing {side} at {coord}')
        self.__board[coord[1], coord[0]] = side.value
        print(self)
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
        return np.all(self.__board != 0)

    def __repr__(self) -> str:
        return str(self.__board)