from abc import ABCMeta, abstractmethod
import numpy as np
import random

from gomoku.board import GomokuBoard
from gomoku.util import Side

class BaseAgent(metaclass=ABCMeta):
    def __init__(self, side: Side = Side.BLACK):
        self.set_side(side)

    def set_side(self, side: Side):
        assert side.is_player()
        self._side = side

    def get_side(self) -> Side:
        return self._side

    @abstractmethod
    def move(self, board: GomokuBoard):
        raise NotImplementedError("Agent must have move() method")

    def get_opponent(self) -> Side:
        return self._side.get_opponent()

class RandomAgent(BaseAgent):
    def move(self, board: GomokuBoard) -> np.array:
        return random.choice(np.array(np.where(board.get_board() == 0)).T)

class ConsoleAgent(BaseAgent):
    def move(self, board: GomokuBoard) -> np.array:
        while True:
            print(f'Player {self._side}, type your next move! Format: [row],[column]')
            user_input = input()
            try:
                coords = str(user_input).split(',')
                return np.array([int(coords[0]), int(coords[1])])
            except:
                print('Invalid input! Format: [row],[column]')