from abc import ABCMeta, abstractmethod
import numpy as np

class BaseAgent(metaclass=ABCMeta):
    @abstractmethod
    def move(self, board):
        pass

class RandomAgent(BaseAgent):
    def move(self, board):
        return np.random.randint(0, board.get_size(), 2)

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
            except:
                print('Invalid input! Format: [x-coord],[y-coord]')