import numpy as np

from board import GomokuBoard
from agent.base import BaseAgent, RandomAgent, ConsoleAgent
from agent.greedy import GreedyAgent, GreedyDefendingAgent

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
    agent1 = GreedyDefendingAgent(1)
    agent2 = ConsoleAgent(2)

    assert isinstance(agent1, BaseAgent)
    assert isinstance(agent2, BaseAgent)

    while True:
        if make_agent_move(game, agent1, 1):
            break
        if make_agent_move(game, agent2, 2):
            break
    print('Game done')
