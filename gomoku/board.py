import numpy as np
import sys

class GomokuBoard:
    __NUM_REQUIRED = 5
    __DIRECTIONS = np.array([[1,0], [1,1], [0,1], [-1,1]])

    def __init__(self, size):
        if size < self.__NUM_REQUIRED:
            print(f'Invalid size: {size}')
            sys.exit()
        self.__size = size
        self.__board = np.zeros((self.__size, self.__size), np.int8)

    def get_board(self):
        return self.__board

    def get_size(self):
        return self.__size

    def add_piece(self, coord, side):
        if not self.is_on_board(coord) or self.get_piece(coord) > 0:
            print(f'Invalid coordinate: {coord}')
            return False

        print(f'Placing {side} at {coord}')
        self.__board[coord[1], coord[0]] = side
        print(self)
        return True

    def is_on_board(self, coord):
        return coord[0] >= 0 and coord[0] < self.__size \
            and coord[1] >= 0 and coord[1] < self.__size

    def get_piece(self, coord):
        if not self.is_on_board(coord):
            return 0
        return self.__board[coord[1], coord[0]]

    def check_win(self, coord, side):
        for direction in self.__DIRECTIONS:
            piece_count = 0
            for offset in range(-self.__NUM_REQUIRED+1, self.__NUM_REQUIRED):
                if self.get_piece(coord + direction * offset) == side:
                    piece_count += 1
                    if piece_count == self.__NUM_REQUIRED:
                        return True
                else:
                    piece_count = 0
        return False

    def check_tie(self):
        return np.all(self.__board != 0)

    def __repr__(self):
        return str(self.__board)