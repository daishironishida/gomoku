from abc import ABCMeta, abstractmethod
import numpy as np

class GameManager:
    def __init__(self, size=19):
        self.__board = GomokuBoard(size)

    def get_board(self):
        return self.__board

    def add_piece(self, coord, side):
        """
        Place a piece on the board and check ending criteria

        Parameters
        ----------
        coord : np.array
            coordinate to place the piece
        side : int
            side of the piece

        Returns
        -------
        success: bool
            validity of the move
        winner: int
            winning side if it exists, -1 if tied, 0 otherwise
        board: GomokuBoard
            state of the board after the move
        """

        if not self.__board.add_piece(coord, side):
            return False, 0, self.__board

        if self.__board.check_win(coord, side):
            winner = side
            print(f'{side} wins!')
        elif self.__board.check_tie():
            winner = -1
            print('game tied!')
        else:
            winner = 0

        return True, winner, self.__board

class GomokuBoard:
    __NUM_REQUIRED = 5
    __DIRECTIONS = np.array([[1,0], [1,1], [0,1], [-1,1]])
    
    def __init__(self, size):
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

class BaseAgent(metaclass=ABCMeta):
    @abstractmethod
    def move(self, board):
        pass

class RandomAgent(BaseAgent):
    def __init__(self, size):
        self.__size = size

    def move(self, board):
        return np.random.randint(0, self.__size, 2)

class ConsoleAgent(BaseAgent):
    def __init__(self, side):
        self.__side = side
        print(f'Initializing console agent for side {self.__side}')
    
    def move(self, board):
        while True:
            print(f'Player {self.__side}, type your next move! Format: [x-coord],[y-coord]')
            user_input = input()
            try:
                coords = str(user_input).split(',')
                return np.array([int(coords[0]), int(coords[1])])
            except Exception as e:
                print('Invalid input! Format: [x-coord],[y-coord]')

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
                        elif board.get_piece(base) > 0:
                            combinations[dir_idx, row, col] = -1
                            break

        for dir, row, col in zip(*np.where(combinations//32 == np.amax(combinations//32))):
            flags = combinations[dir, row, col] % 32
            for offset in range(5):
                if flags & (1 << offset) == 0:
                    coord = np.array([col, row]) + offset * self.__DIRECTIONS[dir]
                    if board.is_on_board(coord):
                        return coord

if __name__ == "__main__":
    # sample run
    def make_agent_move(game, agent, side):
        board = game.get_board()
        while True:
            move = agent.move(board)
            success, winner, board = game.add_piece(move, side)
            if success:
                return winner != 0

    GAME_SIZE = 7

    game = GameManager(GAME_SIZE)
    agent1 = GreedyAgent(1)
    agent2 = ConsoleAgent(2)

    assert isinstance(agent1, BaseAgent)
    assert isinstance(agent2, BaseAgent)

    while True:
        if make_agent_move(game, agent1, 1):
            break
        if make_agent_move(game, agent2, 2):
            break
    print('Game done')
