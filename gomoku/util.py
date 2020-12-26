from enum import Enum
import numpy as np

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