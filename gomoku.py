import numpy as np

class GomokuBoard:
    __NUM_REQUIRED = 5
    __DIRECTIONS = np.array([[1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]])
    
    def __init__(self, size=19):
        self.__size = size
        self.__board = np.zeros((self.__size, self.__size), np.int8)

    def get_board(self):
        return self.__board

    def get_size(self):
        return self.__size

    def add_piece(self, coord, side):
        print(f'Placing {side} at {coord}')
        self.__board[coord[0], coord[1]] = side
        print(self)
        if self.__check_win(coord, side):
            print(f'{side} wins!')

    def __is_on_board(self, coord):
        return coord[0] >= 0 and coord[0] < self.__size \
            and coord[1] >= 0 and coord[1] < self.__size
    
    def __get_piece(self, coord):
        if not self.__is_on_board(coord):
            print(f'Invalid coordinate: {coord}')
            return 0
        return self.__board[coord[0], coord[1]]

    def __check_win(self, coord, side):
        for direction in self.__DIRECTIONS:
            is_win = True
            for offset in range(1, self.__NUM_REQUIRED):
                if not self.__get_piece(coord + direction * offset) == side:
                    is_win = False
                    break
            if is_win:
                return True
        return False

    def __repr__(self):
        return str(self.__board)

if __name__ == "__main__":
    # sample run
    board = GomokuBoard(7)
    for i in range(1,6):
        board.add_piece(np.array((i,2)), 1)
