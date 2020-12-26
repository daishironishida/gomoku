from abc import ABCMeta, abstractmethod
import numpy as np

from gomoku.board import GomokuBoard
from gomoku.util import Side

class BaseAgent(metaclass=ABCMeta):
    def __init__(self, side: Side):
        assert side.is_player()
        self._side = side

    @abstractmethod
    def move(self, board: GomokuBoard):
        raise NotImplementedError("Agent must have move() method")

    def get_opponent(self) -> Side:
        return self._side.get_opponent()

class RandomAgent(BaseAgent):
    def move(self, board: GomokuBoard) -> np.array:
        return np.random.randint(0, board.get_size(), 2)

class ConsoleAgent(BaseAgent):
    def move(self, board: GomokuBoard) -> np.array:
        while True:
            print(f'Player {self._side}, type your next move! Format: [x-coord],[y-coord]')
            user_input = input()
            try:
                coords = str(user_input).split(',')
                return np.array([int(coords[0]), int(coords[1])])
            except:
                print('Invalid input! Format: [x-coord],[y-coord]')