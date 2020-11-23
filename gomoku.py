import numpy as np

class GomokuBoard:
    NUM_REQUIRED = 5
    DIRECTIONS = np.array([[1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]])
    
    def __init__(self, size=19):
        self.size = size
        self.board = np.zeros((self.size, self.size), np.int8)
    
    def is_on_board(self, coord):
        return coord[0] >= 0 and coord[0] < self.size \
            and coord[1] >= 0 and coord[1] < self.size
    
    def get_piece(self, coord):
        if not self.is_on_board(coord):
            print(f'Invalid coordinate: {coord}')
            return 0
        return self.board[coord[0], coord[1]]
    
    def add_piece(self, coord, side):
        print(f'Placing {side} at {coord}')
        self.board[coord[0], coord[1]] = side
        print(self)
        if self.check_win(coord, side):
            print(f'{side} wins!')
    
    def check_win(self, coord, side):
        for direction in self.DIRECTIONS:
            is_win = True
            for offset in range(1, self.NUM_REQUIRED):
                if not self.get_piece(coord + direction * offset) == side:
                    is_win = False
                    break
            if is_win:
                return True
        return False

    def __repr__(self):
        return str(self.board)

if __name__ == "__main__":
    # sample run
    board = GomokuBoard(7)
    for i in range(1,6):
        board.add_piece(np.array((i,2)), 1)
