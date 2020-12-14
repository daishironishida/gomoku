from abc import ABCMeta, abstractmethod
import numpy as np

class GomokuBoard:
    __NUM_REQUIRED = 5
    __DIRECTIONS = np.array([[1,0], [1,1], [0,1], [-1,1]])
    
    def __init__(self, size=19):
        self.__size = size
        self.__board = np.zeros((self.__size, self.__size), np.int8)

    def get_board(self):
        return self.__board

    def get_size(self):
        return self.__size

    def add_piece(self, coord, side):
        """
        Place a piece on the board

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
        board: np.array
            state of the board after the move
        """

        if not self.__is_on_board(coord) or self.__get_piece(coord) > 0:
            print(f'Invalid coordinate: {coord}')
            return False, 0, self.__board

        print(f'Placing {side} at {coord}')
        self.__board[coord[1], coord[0]] = side
        print(self)

        if self.__check_win(coord, side):
            winner = side
            print(f'{side} wins!')
        elif self.__check_tie():
            winner = -1
            print('game tied!')
        else:
            winner = 0

        return True, winner, self.__board

    def __is_on_board(self, coord):
        return coord[0] >= 0 and coord[0] < self.__size \
            and coord[1] >= 0 and coord[1] < self.__size
    
    def __get_piece(self, coord):
        if not self.__is_on_board(coord):
            return 0
        return self.__board[coord[1], coord[0]]

    def __check_win(self, coord, side):
        for direction in self.__DIRECTIONS:
            piece_count = 0
            for offset in range(-self.__NUM_REQUIRED+1, self.__NUM_REQUIRED):
                if self.__get_piece(coord + direction * offset) == side:
                    piece_count += 1
                    if piece_count == self.__NUM_REQUIRED:
                        return True
                else:
                    piece_count = 0
        return False

    def __check_tie(self):
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

    gomoku_board = GomokuBoard(GAME_SIZE)
    agent1 = RandomAgent(GAME_SIZE)
    agent2 = ConsoleAgent(2)

    assert isinstance(agent1, BaseAgent)
    assert isinstance(agent2, BaseAgent)

    while True:
        if make_agent_move(gomoku_board, agent1, 1):
            break
        if make_agent_move(gomoku_board, agent2, 2):
            break
    print('Game done')
