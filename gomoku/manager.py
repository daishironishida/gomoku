import numpy as np

from gomoku.board import GomokuBoard

class GameManager:
    def __init__(self, size: int = 19):
        self.__board = GomokuBoard(size)

    def get_board(self):
        return self.__board

    def add_piece(self, coord, side: int) -> (bool, int, GomokuBoard):
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
