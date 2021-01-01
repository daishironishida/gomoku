from enum import Enum
import numpy as np
import os
from datetime import datetime

# number of pieces in a row for win
NUM_REQUIRED = 5

# valid directions
DIRECTIONS = np.array([[1,0], [1,1], [0,1], [-1,1]])

class Side(Enum):
    # Players
    BLACK = 1
    WHITE = 2

    # Piece on the board
    NONE = 0

    # Winners
    TIE = -1

    def is_player(self) -> bool:
        return self.value > 0

    def is_piece(self) -> bool:
        return self.value > -1

    def get_opponent(self) -> bool:
        assert self.is_player()
        if self == Side.BLACK:
            return Side.WHITE
        else:
            return Side.BLACK

    def __str__(self) -> str:
        return self.name

class CsvStream():
    def __init__(self, directory: str, size: int):
        os.makedirs(directory, exist_ok=True)
        self.__file = os.path.join(directory, datetime.now().strftime('%y%m%d%H%M%S'))

        with open(self.__file, 'w') as f:
            f.write(f'{size}\n')

    def add_move(self, side: Side, coord: np.array, board: np.array, winner: Side):
        assert(side.is_player())

        with open(self.__file, 'a') as f:
            f.write(f'{side.value},{coord[1]},{coord[0]}\n')
            for row in board:
                f.write(','.join([str(x) for x in row]) + '\n')
            f.write(f'{winner.value}\n')
